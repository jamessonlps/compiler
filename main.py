import sys
from _parser import Parser
from assembler import assembler

if __name__ == "__main__":
    code = ""
    filename = ""
    with open(sys.argv[1], "r") as file:
        filename = sys.argv[1].split("/")[-1].split(".")[0]
        code = Parser.run(file.read())
    
    lines = code.splitlines()
    lines_without_spaces = [line.strip() for line in lines]
    code_without_spaces = "\n".join(lines_without_spaces)

    asm = assembler.write(code_without_spaces, filename=filename)

    # print(asm)