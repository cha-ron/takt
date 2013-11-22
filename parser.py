ocurl = "{"
ccurl = "}"
opern = "("
cpern = ")"
pipe = "|"

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
