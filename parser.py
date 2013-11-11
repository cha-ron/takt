import lexer

def parseSource(source):
	return parse(lexer.lex(source))

def parse(tokenStream):

