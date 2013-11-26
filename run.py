import sys

import lexer
import parser
import state

prompt = "> "
exit = "exit"

grammar = parser.parseGrammar("spec.txt")

def lexandparse(string):
	statement_stream = lexer.lex(string)
	for statement in statement_stream:
		statement = lexer.assignNameSpecs(statement, state.names)

		if statement != None:
			ptree = parser.parse(statement, grammar)
	
			if ptree != None:
				ptree = parser.massage(ptree, grammar, lexer.punctuation)
				output = state.evaluate(ptree)
	
				if output != None:
					if type(output) == type([]):
						for i in output:
							print(i)
					else:
						print(output)

def repl():
	while True:
		inp = input(prompt)
		if inp == exit:
			break
		else:
			lexandparse(inp)

def main():
	if len(sys.argv) > 1:
		f = open(sys.argv[0],'r')
		lexandparse(f.read())
		f.close()
		if len(sys.argv) != 1:
			repl()
	else:
		repl()

if __name__ == "__main__":
	main()
