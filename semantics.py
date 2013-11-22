# for storing the phonetic universe 
class Universe:
	def __init__(self, name_in="", exist_in=False, contents_in=[]):
		self.name = name_in
		self.exist = exist_in
		self.contents = contents_in

	def newUniverse(name_in, exist_in):
		return NaturalClass(name_in, exist_in)


class Feature:
	def __init__(self, name_in="", spec_in=False):
		self.name = name_in
		self.spec = spec_in

class FeatureVector:
	def __init__(self, contents_in=[]):
		self.contents = contents.in

class FeatureVectorString:
	def __init__(self, contents_in=[]):
		self.contents = contents.in

class Environment:
	def __init__(self, left_in=FeatureVectorString(), right_in=FeatureVectorString()):
		self.left = left.in
		self.right = right_in

class SoundChange:
	def __init__(self, start_in=FeatureVector(), end_in=FeatureVector(), env_in=Environment()):
		self.start = start_in
		self.end = end_in
		self.env = env_in
