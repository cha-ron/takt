import lexer

ocurl = "{"
ccurl = "}"
opern = "("
cpern = ")"
pipe = "|"

def parseSource(source):
	return parse(lexer.lex(source))

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
		print(splitline)
		if splitline != []:
			head = splitline[0]
			tail = parseGramTail(splitline[2:])
	
			retgram[head] = tail

	return retgram
