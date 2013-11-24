ocurl = "{"
ccurl = "}"
opern = "("
cpern = ")"
pipe = "|"

# pretty print a parse tree
def pppt(t,i=0):
	print(('\t'*i) + "( " + t[0], end='')

	if type(t[1]) == type([]):
		print()
		for q in t[1]:
			pppt(q,i+1)
		print(('\t'*i) + ")")
	else:
		print(" '" + t[1] + "' )")

def ntmatch(rulelist, partition, grammar):
	b = True

	for i in range(len(rulelist)):
		r = rulelist[i]

		if r not in grammar:
			b = (b and (derives(partition[i], r, grammar) != False))

	return b

# recursively checks if the partition matches the rule
def derives(partition, rule, grammar):
	lp = len(partition)

	if rule not in grammar: # if matching a single token to a terminal
		if lp == 1 and (partition[0].typestr == rule):
			return (partition[0].typestr, partition[0].text)
		else: # more than one token can never match a single terminal
			return False
	else: # matching multiple tokens to a nonterminal: try and match partitions to what that rule outputs
		for rulelist in grammar[rule]: # rules often expand into more than one form; this looks at each of them
			rll = len(rulelist)

			if lp >= rll: # n tokens cannot be matched onto m rules if m > n
				parts = partset(partition, rll) # all of the partitions into rll slots

				for p in parts: # iterate over possible partitions
					combs = []

					if not ntmatch(rulelist, p, grammar):
						continue

					for i in range(rll):
						combs += [derives(p[i], rulelist[i], grammar)]
					if False not in combs:
						return (rule, combs)
					else:
						continue
				
	return False
					



# partitions a range from s to e into m slots
# (e - s + 1) >= m
def partition(s, e, m):
	l = e - s + 1
	if (l == 1) or (m == 1):
		return [[(s,e+1)]]
	if l == m:
		return [[(i,i+1) for i in range(s, e+1)]]
	else:
		ret = []

		for i in range(l - m + 1):
			start = [(s,s+i+1)]
			ends = partition(s+i+1, e, m-1)

			for end in ends:
				ret += [start + end]

		return ret

def partset(s, m):
	parts = partition(0,len(s)-1, m)
	ret = []

	for p in parts:
		np = []

		for rang in p:
			np += [s[rang[0]:rang[1]]]

		ret += [np]

	return ret

def getindices(c,st,en):
	return (c.index(st),c.index(en))

def tripart(c,s,e):
	return (c[:s],c[s+1:e],c[e+1:])

def atp(c,st,en): # = auto tripart
	s,e = getindices(c,st,en)
	return tripart(c,s,e)

def parseGramTail(tail):
	ret = []

	ret.append(tail.copy())

	if (ocurl in tail) or (pipe in tail) or (opern in tail):
		stack = [ret.pop()]

		while len(stack) != 0:
			curr = stack.pop()

			if (ocurl not in curr) and (pipe not in curr) and (opern not in curr):
				ret.append(curr)
				continue

			if opern in curr:
				bef,mid,aft = atp(curr, opern, cpern)

				stack.append(bef + aft)
				stack.append(bef + mid + aft)
				continue

			if ocurl in curr:
				bef,mid,aft = atp(curr, ocurl, ccurl)

				for part in procAlts(mid):
					stack.append(bef + part + aft)

				continue

			if pipe in curr:
				for alt in procAlts(curr):
					ret.append(alt)


	return ret

def procAlts(stream):
	ret = []
	end = stream.copy()

	while len(end) != 0:
		if pipe in end:
			i = end.index(pipe)
			ret.append(end[:i])
			end = end[i+1:]
		else:
			ret.append(end)
			break

	return ret


def parseGrammar(grammar_loc):
	retgram = {}

	grammar = open(grammar_loc,'r')

	for line in grammar:
		splitline = line.split()
		if splitline != []:
			head = splitline[0]
			tail = parseGramTail(splitline[2:])
	
			retgram[head] = tail

	return retgram

def invertGrammar(grammar):
	ret = {}

	for key in grammar:
		for parse in grammar[key]:
			p = tuple(parse)

			if p in ret:
				print(str(p) + " is ambiguous")

			ret[p] = key

	return ret

def massage(ptree, grammar, punctuation):
	rrules = findRecursiveRules(grammar)

	ptree = flattenRecursives(ptree, rrules)[0]
	ptree = removePunctuation(ptree, punctuation)[0]

	return ptree

def removePunctuation(ptree, punctuation):
	if ptree[0].startswith(tuple(punctuation)):
		return []
	elif type(ptree[1]) == type([]):
		l = ptree[1].copy()
		r = []

		while len(l) != 0:
			r = removePunctuation(l.pop(), punctuation) + r

		return [(ptree[0], r)]
	else:
		return [ptree]

def findRecursiveRules(grammar):
	ret = {}

	for rule in grammar:
		for r in grammar[rule]:
			if rule in r:
				if rule in ret:
					ret[rule] += [r]
				else:
					ret[rule] = [r]

	return ret

# flattens recursive definitions (i.e. how i allowed n-length strings of things in the grammar)
# might be scrapped if i can get the parser to do this itself
# which might provide some pretty big savings in time (i think the recursive definitions are the major hangup at the moment)
def flattenRecursives(ptree, rrules):
	if type(ptree[1]) == type(""): # if terminal
		return [ptree]
	else:
		l = ptree[1].copy()
		r = []

		while len(l) != 0:
			r = flattenRecursives(l.pop(), rrules) + r

		if ptree[0] in rrules:
			return r
		else:
			return [(ptree[0], r)]
