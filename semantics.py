class TypedObj:
	def __init__(self, typestr_in):
		self.typestr = typestr_in
		self.probability = 0

	def aprob(self, p):
		self.probability = p

	def norm(self, f):
		self.probability /= f

	def weighted(self):
		return (self.probability == 0)

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
			self.quants[name] = True
		elif quant == 'quantifier-existential':
			self.quants[name] = False

	# must all of the children of this natural class's parent be defined?
	# i.e. does it not zero-out its siblings?
	# i.e. was its parent marked universal?
	def poly(self, name):
		if name not in self.parents:
			return True
		else:
			return self.quants[self.parent(name)]

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
		if parent == None:
			return []
		else:
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
		if child in parents:
			return self.parents[child]
		else:
			return None

	# generates every possible fully-specified segment in this universe
	def genall(self, seg=None,level=''):
		if level == '':
			level = self.root
			seg = Segment(self,[(level, True)])

		children = self.listchildren(level)

		if len(children) == 0:
			return [seg, seg.speccp(univ, level, False)]
		else:
			if self.poly(level):
				sel = [genall(seg.speccp(univ, child, True), child) for child in children]
				ret = sel.pop()

				while len(sel) != 0:
					t = sel.pop()
					rs = [ret.copy() for i in t]

					for copy in range(len(t)):
						for i in range(len(ret)):
							rs[copy][i] = rs[copy][i].apply(univ, t[copy])

					ret = []
					for c in rs:
						ret.extend(c)

				return ret


				return ret
			else:
				ret = []

				for child in children:
					s = seg.copy()
					s.specify(child, True)
					ret.extend(self.genall(s, child))

				return ret


		

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

# dummy class to hold naturalclasses
class NaturalClass(TypedObj):
	def __init__(self):
		super().__init__("natural-class")

# holds a language allowance
class Language:
	def __init__(self):
		self.allowed = []

	def add(self, target):
		self.allowed += [target]

	def match(self, target):
		m = False

		for segment in self.allowed:
			m = m or target.match(segment)

def pom(s):
	if s:
		return "+"
	else:
		return "-"

# holds all the information for a segment
class Segment(TypedObj):
	# specs_in is a list of tuples of specs, where:
	# 	spec[0] is the name of the feature
	#	spec[1] is True if it's + and False if it's -
	def __init__(self, univ=None, specs_in=[]):
		super().__init__("feature-vec")

		self.specs = {}

		if univ != None:
			for spec in specs_in:
				self.specify(univ, spec[0], spec[1])

	def __str__(self):
		strrep = ""

		for spec in self.specs:
			strrep += pom(self.specs[spec]) + spec + ","

		strrep = strrep.rstrip(",")

		return "[" + strrep + "]"

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

	def speccp(self, univ, n, s):
		r = self.copy()
		r.specify(univ, n, s)
		return ret

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

	# returns a copy of the segment
	def copy(self):
		ret = Segment()

		for name in self.specs:
			ret.specs[name] = self.specs[name]

		return ret

	# is the segment fully specified (does it define only one phoneme?)
	def specified(self, univ):
		r = True

		for name in self.specs:
			r = r and (name in univ.tree)

		return r

	# generate all possible specifications for this segment
	# in the form of a list of segments
	def genall(self, univ):
		if self.specified(univ):
			return [self]
		else:
			allpos = univ.genall()
			ret = []

			for pos in allpos:
				if self.match(pos):
					ret.extend(pos)

			return ret

# a string of segments = a feat-vec-str
class SegmentStr(TypedObj):
	def __init__(self, segs=[]):
		super().__init__("feat-vec-str")

		self.segments = []
		self.length = 0

		for segment in segs:
			self.segments.append(segment)

	def match(self, targetstr):
		if self.length > targetstr.length:
			return False

		if self.findmatch(targetstr) != -1:
			return True

		return False

	# finds the index of the start of a match; returns -1 if no match is found
	def findmatch(self, targetstr):
		for i in range(targetstr.length):
			m = True

			for j in range(self.length):
				m = m and self.segments[j].match(targetstr.segments[i+j])

			if m:
				return i

		return -1
		

	def add(self, target):
		if isinstance(target, Segment):
			self.segments += [target]
			self.length += 1
		if isinstance(target, SegmentStr):
			for segment in target.segments:
				self.add(segment)
			self.length += target.length

	def copy(self):
		ret = SegmentStr()
		ret.add(self)
		return ret

	def genall(self, univ):
		return [segment.genall(univ) for segment in segments]

class Environment(TypedObj):
	def __init__(self, left_in, right_in):
		super().__init__("environment")

		self.left = left_in
		self.right = right_in

	# whether the environment matches
	def match(self, target):
		m = self.findmatch(target)

		if m == -1:
			return False
		else:
			return True

	# returns the matching segment
	def extract(self, target):
		m = self.findmatch(target)

		if m == -1:
			return None
		else:
			return target.segments[m].copy()

	# partitions the target into three parts:
	#	1. a segment string containing the segments before a match
	#	2. the segment that matches
	#	3. a segment string containing the segments after the match
	# returns None if no match
	def partition(self, target):
		m = self.findmatch(target)

		if m == -1:
			return None
		else:
			return (SegmentStr(target.segs[0:m]), target.segs[m], SegmentStr(target.segs[m+1:target.length]))

	# returns the index of the matched segment
	# i.e. what's in the place of the underscore in : [+x]/[+y]/[+a]_[+b]
	# -1 if no match
	def findmatch(self, target):
		l = left.findmatch(target)
		r = right.findmatch(target)

		if (l == -1) or (r == -1):
			return -1

		ind = l + left.length

		if r == ind + 1:
			return ind


class SoundChange(TypedObj):
	def __init__(self, frm_in, to_in, env_in):
		super().__init__("sound-change")

		self.frm = frm_in
		self.to = to_in
		self.env = env_in

	# applies a sound change to a target
	# if the target is a segment, applies just the sound change without matching the environment
	# else, matches env, applies change
	# if no match (to from, or to environment), returns target
	def apply(self, target):
		if isinstance(target, Segment):
			if target.match(self.frm):
				return self.to.apply(target)
			else:
				return target
		if isinstance(target, SegmentStr):
			m = self.env.partition(target)

			if m == None:
				return target
			else:
				if self.frm.match(m[1]):
					ret = m[0]
					ret.add(self.to.apply(m[1]))
					ret.add(m[2])

					return ret
				else:
					return target

