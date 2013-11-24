import semantics

# the program has four pieces of state:
#	1. the names dictionary
#	2. the phonological universe
#	3. the sonority hierarchy
#	4. the language

names = {}
universe = semantics.Universe()
sonority = semantics.Sonority()

# only two things are changed when a statement is evaluated, possibly. either:
#	1. the statement requires a change in the program's state
#	2. the statement requires some output
# the only thing ever actually returned by eval is output; if the statement 
# requires no output, eval will return nothing, and will in effect return None
# this must be checked when printing output

# this is basically a giant case-switch statement on the first item of the input ptree
# the program state variables aren't input into eval because they're globals
# (this might not work - i'll have to see)
def evaluate(ptree):
	ptree[0] = name

	# trivial initial case
	if name == 'statement':
		below = obg(ptree)
		return evaluate(below)

	# pure queries are the only things that actually produce output
	if name == 'query':
		below = ob2(ptree)
		return evaluate(ob2(ptree)) # queries always wrap a typed query which wrap the meat of the query
						# (typed queries are 'query-feature-vec' etc.)

	# name assignments are the only thing that will change the names dictionary
	if name == 'name-assign':
		name_in = obg(ptree,True)
		below = 2bg(ptree)
		names[name_in] = evaluate(below)

	# universe definitions change the phonological universe
	# also, the sonority hierarchy must be updated
	if name == 'universe-def':
		name_in = obg(ptree, True)
		quant = 2gb(ptree)[0]

		if len(ptree[1]) == 2:
			universe.add(name_in, quant)
			sonority.update(name_in)
		if len(ptree[1]) == 3
			name_below = ptree[1][2][1]

			universe.add(name_in, quant, name_below)
			sonority.update(name_in, name_below)

	# sonority definitions change the sonority hierarchy
	if name == 'sonority-def':
		comps = ptree[1]

		for i in range(0, len(comps) - 1, 2):
			son = comps[i+1][0]
			l = comps[i][1]
			r = comps[i+2][1]

			if son == 'sonority-up':
				sonority.rank(univ, l, r)
			if son == 'sonority-down':
				sonority.rank(univ, r, l)

	# language allowances change the language
	if name == 'language-allowance':

	# if the ptree is a name of something
	# works since the only other thing that starts with 'name' is 'name-assign'
	# and those are caught above
	if name.startswith('name'):
		return names[ptree[1]]

# to be used when the ptree in question has only one ptree in its body
# or, when you just want the first thing in its body
def obg(ptree, term=False): # = one body grab
	if term:
		return ptree[1][0][1]
	else:
		return ptree[1][0]

# grabs the second thing in this ptree's body
# useful because lots of things end up being binary
def 2bg(ptree):
	return ptree[1][1]

# same as obg but it goes two levels down
def ob2(ptree,term=False):
	return obg(obg(ptree,term))

# n levels down
def obn(ptree, n, term=False):
	if n == 1:
		return obg(ptree,term)
	else:
		return obn(ptree, n-1, term)
