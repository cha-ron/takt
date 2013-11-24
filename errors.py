def name_error(linestr, offendor):
	print("err: name error in line '" + linestr + "': '" + offendor + "' used before assignment")

def parse_error(linestr):
	print("err: '" + linestr + "' is ungrammatical")
