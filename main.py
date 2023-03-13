import sys
from _parser import Parser

if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        Parser.run(file.read())