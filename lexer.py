import errors

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
		"#":"seperator-probability",
		"&":"seperator-concatenate",
		"@":"seperator-generate",
		"*":"seperator-apply",
		"$":"seperator-allow",
		"%":"seperator-query"}
null_type = "null"
name_type = "name"
number_type = "number"

punctuation = ["seperator", "begin", "end"]

# class to hold lex tokens
class Token:
	typestr = null_type
	text = ""

	def __init__(self, typestr_in=null_type, text_in=""):
		self.typestr = typestr_in
		self.text = text_in
	
	def __str__(self):
		return "(" + self.typestr + ": '" + self.text + "'" + ")"

# strips all (including interior) whitespace from a string
def stripwhite(string):
	l = string.split()
	ret = ""

	for i in l:
		ret += i
	
	return ret

def printStatementList(statement_list):
	for statement in statement_list:
		for token in statement:
			print(token.typestr + ":'" + token.text + "'")
		print()

def lexliteral(tl,cm,curr=""):
	if cm.isdecimal():
		return (tl + [Token(number_type,cm)],"")
	elif cm.isalnum():
		return (tl + [Token(name_type,cm)],"")
	else:
		return (tl,cm)

def printss(ss):
	for statement in ss:
		for literal in statement:
			print(literal)
		print()

# lexes a source string; returns an array of statements, which are arrays of tokens
def lex(source):
	ret = []

	statement_list = stripwhite(source).split(".")

	if statement_list[-1] == '':
		statement_list = statement_list[:-1]

	for statement in statement_list:
		tok_list = []
		current_multi = ""

		for char in statement:
			if char in special_chars:
				tok_list,current_multi = lexliteral(tok_list,current_multi)

				tok_list += [Token(special_chars[char], char)]
			else:
				current_multi += char

		tok_list,current_multi = lexliteral(tok_list,current_multi)
		ret += [tok_list]

	return ret

# reconstructs the string-form of a statement from a token stream
def reconstructStatementString(statement):
	ret = statement[0].text
	for token in statement[1:]:
		ret += (" " + token.text)

	return ret

# gives types to names
# 'names' is named-entities dictionary
def assignNameSpecs(statement, names):
	for token in statement:
		if token.typestr == name_type:
			# undefined names may only appear statement-initially behind name-assignment seperators
			if not ((token == statement[0]) and (statement[1].typestr in [special_chars[":"], special_chars["!"], special_chars["?"]])):
				if token.text not in names:
					errors.name_error(reconstructStatementString(statement), token.text)
					return None
				else:
					token.typestr += ("-" + names[token.text].typestr)
	return statement

