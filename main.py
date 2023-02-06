import sys
import re

def check_sum():
    if (len(sys.argv) > 2):
        raise Exception("Insira apenas um parâmetro com a operação entre strings.")
    
    operation: str = sys.argv[1]
    
    # Limpa espaços em branco
    string_clear = operation.replace(" ", "")
    # string_splitted = re.findall(pattern=r"[0-9]|[+-]", string=string_clear)

    return eval(string_clear)

check_sum()