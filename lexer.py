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

	def __init__(self, typestr_in=null_type, text_in=""):
		self.typestr = typestr_in
		self.text = text_in

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

def lexliteral(tl,cm):
	if cm.isdecimal():
		return (tl + [Token(number_type,cm)],"")
	if cm.isalnum():
		return (tl + [Token(name_type,cm)],"")
	else:
		return (tl,cm)


# lexes a source string; returns an array of statements, which are arrays of tokens
def lex(source):
	ret = []

	statement_list = stripwhite(source).split(".")
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
