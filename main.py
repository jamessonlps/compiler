import sys
from _parser import Parser
from SymbolTable import symbol_table

if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        root = Parser.run(file.read())

    root.evaluate(symbol_table=symbol_table)