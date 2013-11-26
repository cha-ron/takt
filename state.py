import semantics
import random

# the program has four pieces of state:
#	1. the names dictionary
#	2. the phonological universe
#	3. the sonority hierarchy
#	4. the language

names = {}
universe = semantics.Universe()
sonority = semantics.Sonority(universe)
language = semantics.Language()

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
	name = ptree[0]

	# trivial initial case
	if name == 'statement':
		below = obg(ptree)
		return evaluate(below)

	# pure queries are the only things that actually produce output
	if name == 'query':
		below = ob2(ptree)
		return evaluate(below) # queries always wrap a typed query which wrap the meat of the query
						# (typed queries are 'query-feature-vec' etc.)

	if name == 'query-feature-vec':
		below = obg(ptree)
		return evaluate(below)

	if name == 'query-feat-vec-str':
		below = obg(ptree)
		return evaluate(below)

	# only generations begin with 'generate'
	if name.startswith('generate'):
		count = evaluate(obg(ptree))
		target = evaluate(tbg(ptree))

		return generate(target, count)

	# only applications begin with 'apply', and they both can be treated in the same way
	if name.startswith('apply'):
		sc = evaluate(obg(ptree))
		target = evaluate(tbg(ptree))

		return sc.apply(target)

	# name assignments are the only thing that will change the names dictionary
	if name == 'name-assign':
		name_in = obg(ptree,True)
		below = tbg(ptree)
		names[name_in] = evaluate(below)

	if name == 'sound-change':
		below = obg(ptree)
		ret = evaluate(below)

		if hasprob(ptree):
			ret.aprob(evaluate(obl(ptree)))

		return ret

	if name == 'sound-change-def':
		frm = evaluate(ptree[1][0])
		to = evaluate(ptree[1][1])
		env = evaluate(ptree[1][2])

		return semantics.SoundChange(frm, to, env)

	if name == 'feature-vec':
		below = obg(ptree)
		ret = evaluate(below)

		if hasprob(ptree):
			ret.aprob(evaluate(obl(ptree)))

		return ret

	if name == 'feature-vec-def':
		feats = [evaluate(i) for i in ptree[1]]

		return semantics.Segment(universe, feats)

	if name == 'spec':
		return (tbg(ptree, True), obg(ptree) == 'feature-positive')

	if name == 'environment':
		below = obg(ptree)
		ret = evaluate(below)

		if hasprob(ptree):
			ret.aprob(evaluate(obl(ptree)))

		return ret

	if name == 'environment-def':
		l = evaluate(obg(ptree))
		r = evaluate(tbg(ptree))

		return semantics.Environment(l, r)

	if name == 'feat-vec-str':
		segs = [evaluate(i) for i in ptree[1]]
		ret = semantics.SegmentStr(segs)

		if hasprob(ptree):
			ret.aprob(evaluate(obl(ptree)))

		return ret

	# universe definitions change the phonological universe and names
	# also, the sonority hierarchy must be updated
	if name == 'universe-def':
		name_in = obg(ptree, True)
		quant = tbg(ptree)[0]

		if len(ptree[1]) == 2:
			universe.add(name_in, quant)
			sonority.update(name_in)
		if len(ptree[1]) == 3:
			name_below = ptree[1][2][1]

			universe.add(name_in, quant, name_below)
			sonority.update(name_in, name_below)

		names[name_in] = semantics.NaturalClass()

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
		fv = evaluate(obg(ptree))

		language.add(fv)

	if name == 'prob-assign':
		below = obg(ptree)
		return evaluate(below)

	# if the ptree is a name of something
	# works since the only other thing that starts with 'name' is 'name-assign'
	# and those are caught above
	if name.startswith('name'):
		return names[ptree[1]]

	if name == 'number':
		return int(ptree[1])

def generate(target, count):
	if isinstance(target, semantics.Segment):
		gens = target.genall(universe)

		ret = []
		for i in range(count):
			ret.append(random.choice(gens))

		return ret
	if isinstance(target, semantics.SegmentStr):
		gens = target.genall(universe)

		ret = []
		for i in range(count):
			s = []
			for seg in gens:
				s.extend(random.choice(seg))

		for i in range(self.length):
			ret[i] = SegmentStr(ret[i])

		return ret

def hasprob(ptree):
	return (obl(ptree)[0] == 'prob-assign')

# to be used when the ptree in question has only one ptree in its body
# or, when you just want the first thing in its body
def obg(ptree, term=False): # = one body grab
	if term:
		return ptree[1][0][1]
	else:
		return ptree[1][0]

# grabs the second thing in this ptree's body
# useful because lots of things end up being binary
def tbg(ptree, term=False):
	if term:
		return ptree[1][1][1]
	else:
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

# returns the last object in a ptree's body
def obl(ptree):
	return ptree[1][-1]
