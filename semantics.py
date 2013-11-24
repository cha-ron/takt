# holds the phonological universe
class Universe:
	def __init__(self):
		self.tree = {}
		self.parents = {}
		self.quants = {}
		self.root = ""

	# quant is either 'quantifier-universal' or 'quantifier-existential'
	def add(self, name, quant, below=None):
		# if below nothing, it's the root of the tree
		if below == None:
			self.root = name
		else:
			self.tree[below] += [name]
			self.parents[name] = below

		self.tree[name] = []

		if quant == 'quantifier-universal':
			self.quants[name] == True
		elif quant == 'quantifier-existential':
			self.quants[name] == False

	# must all of the children of this natural class's parent be defined?
	# i.e. does it not zero-out its siblings?
	# i.e. was its parent marked universal?
	def poly(self, name):
		return self.quants(self.parent(name))

	# essentially, does this natural class have any children?
	def binary(self, name):
		return self.tree[name] == []

	# is child a child of parent?
	def ischild(self, parent, child):
		return child in self.tree[parent]

	# is child a child of some child of parent, or so on?
	def below(self, parent, child):
		if self.ischild(parent, child):
			return True
		else:
			b = False
			for c in self.tree[parent]:
				b = b or self.below(c, child)

			return b

	def listchildren(self, parent):
		return self.tree[parent]

	# lists everything below parent
	def listbelow(self, parent):
		ret = [parent]

		if not self.binary(parent):
			children = []

			for child in self.tree[parent]:
				children.extend(self.listbelow(child))

			ret.extend(children)

		return ret

	def parent(self, child):
		return self.parents[child]

# holds and manages a sonority hierarchy
class Sonority:
	def __init__(self, universe):
		self.ranks = {}

		for name in universe.tree:
			self.ranks[name] = 0

	# sets the lowest-ranked name to rank 0
	# preserves order
	def normalize(self):
		mn = min(self.ranks.values())

		if mn != 0:
			for name in self.ranks:
				self.ranks[name] -= mn

	# all names ranked above v
	# if eq, includes names ranked equal to v
	def above(self, v, eq=False, notinc=[]):
		ret = []

		for name in self.ranks:
			if eq:
				if self.ranks[name] >= v:
					ret.append(name)
			else:
				if self.ranks[name] > v:
					ret.append(name)
		
		ret = list(set(ret).difference(set(notinc)))
		return ret

	# all names ranked below v
	# if eq, includes names ranked equal to v
	def below(self, v, eq=False, notinc=[]):
		ret = []

		for name in self.ranks:
			if eq:
				if self.ranks[name] <= v:
					ret.append(name)
			else:
				if self.ranks[name] < v:
					ret.append(name)

		ret = list(set(ret).difference(set(notinc)))
		return ret

	# increments every input rank by the input amount
	# increment defaults to one
	def inc(self, names, i=1):
		if i == 0:
			i = 1

		for name in names:
			self.ranks[name] += i

	# adds a new name to the sonority hierarchy
	def update(self, name, below=None):
		if below == None:
			self.ranks[name] = 0
		else:
			self.ranks[name] = self.ranks[below]

	# the minimum and maximum ranks that the names in the
	# input list have
	def minmax(self, names):
		vals = [self.ranks[name] for name in names]

		return (min(vals), max(vals))


	def maxRankBelow(self, r, notinc):
		return self.minmax(self.below(r,False, notinc))[1]

	def minRankAbove(self, r, notinc):
		return self.minmax(self.above(r,False, notinc))[0]

	# ranks a name above another name
	def rank(self, univ, above, below):
		r = self.ranks[below]

		affected = univ.listbelow(above)
		above_move = self.above(r, False, affected)

		mn,mx = self.minmax(affected)
		mrb = self.maxRankBelow(r, affected)
		mra = self.minRankAbove(r, affected)

		aff_inc = max(0, mrb - mn)
		abv_inc = aff_inc + max(0, mx - mra)

		self.inc(affected, aff_inc)
		self.inc(above_move, abv_inc)

# holds all the information for a segment
class Segment:
	# specs_in is a list of tuples of specs, where:
	# 	spec[0] is the name of the feature
	#	spec[1] is True if it's + and False if it's -
	def __init__(self, univ, specs_in=[]):
		self.specs = {}

		for spec in specs_in:
			self.specify(univ, spec[0], spec[1])

	# specifies a single feature
	def specify(self, univ, n, s):
		# if it zeros-out its siblings and is +
		# (- segments don't zero-out their siblings because that would make them all + and that wouldn't make sense)
		if (not univ.poly(n)) and s:
			children = univ.listchildren(univ.parent(n))
			children.remove(n)

			for name in children:
				self.specify(univ, n, False)

		# even if somewhere below this current feature there's one that's existential (that is, one the children of =
		# which zero each other out), all are marked + or - for the purposes of future comparison
		for name in univ.listbelow(n):
			self.specs[name] = s


	# does other match this segment:
	def match(self, other):
		m = True

		for name in other.specs:
			if name in self.specs:
				m = m and (other.specs[name] == self.specs[name])				

		return m

	# returns the result of the application of other to this segment
	# leaves this original one untouched
	def apply(self, univ, other):
		ret = Segment(univ)

		for seg in [self, other]:
			for name in seg.specs:
				ret.specify(univ)

		return ret
