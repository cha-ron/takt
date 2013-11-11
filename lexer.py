special_chars = {".":"seperator-statement",
		":":"seperator-name",
		"?":"quantifier-universal",
		"!":"quantifier-existential",
		"/":"seperator-sound-change",
		"_":"seperator-environment",
		"[":"begin-feature-vector",
		"]":"end-feature-vector",
		"+":"feature-positive",
		"-":"feature-negative",
		"{":"begin-group",
		"}":"end-group",
		",":"seperator-list",
		">":"seperator-sonority",
		"&":"seperator-concatenate",
		"#":"seperator-probability",
		"@":"seperator-generate",
		"*":"seperator-apply"}
null_type = "null"
name_type = "name"
number_type = "number"

# class to hold lex tokens
class Token:
	typestr = null_type
	text = ""

	def __init__(self, typestr_in, text_in):
		self.typestr = typestr_in
		self.text = text_in

# strips all (including interior) whitespace from a string
def stripwhite(string):
	l = string.split()
	ret = ""

	for i in l:
		ret += i

def printStatementList(statement_list):
	for statement in statement_list:
		print(statement.typstr + ":'" + statement.text + "'")
		print()

# lexes a source string; returns an array of statements, which are arrays of tokens
def lex(source):
	ret = []

	statement_list = source.split(".")
	for statement in statement_list:
		tok_list = []
		current_multi = ""

		for char in statement:
			if char in special_chars:
				if current_multi.isalnum():
					tok_list += [Token(name_type, current_multi)]
					current_multi = ""
				if current_multi.isdecimal():
					tok_list += [Token(number_type, current_multi)]
					current_multi = ""

				tok_list += [Token(special_chars[char], char)]
			else:
				current_multi += char

		if current_multi.isalnum():
			tok_list += [Token(name_type, current_multi)]
			current_multi = ""
		if current_multi.isdecimal():
			tok_list += [Token(number_type, current_multi)]
			current_multi = ""

		ret += [tok_list]

	return ret
