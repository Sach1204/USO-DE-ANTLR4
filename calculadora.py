import sys
from antlr4 import *
from labeldExprLexer import labeldExprLexer
from labeldExprParser import labeldExprParser
from EvalVisitor import EvalVisitor

def main(argv):
    # Determinar la fuente de entrada: archivo o stdin
    if len(argv) > 1:
        data = FileStream(argv[1])
    else:
        data = InputStream(sys.stdin.read())

    # Fase léxica
    lexer = labeldExprLexer(data)
    tokens = CommonTokenStream(lexer)

    # Fase de parsing
    parser = labeldExprParser(tokens)
    tree = parser.prog()

    # Evaluador con visitor
    evaluator = EvalVisitor()
    evaluator.visit(tree)

if __name__ == "__main__":
    main(sys.argv)
