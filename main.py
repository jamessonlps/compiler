import sys
import re
import ast

def check_sum():
    if (len(sys.argv) > 2):
        raise Exception("Insira apenas um parâmetro com a operação entre strings.")
    
    operation: str = sys.argv[1]

    # Verifica se há espaço em branco entre 2 números consecutivos
    string_with_numbers_spaced = re.findall(pattern=r"[0-9]\s+[0-9]", string=operation)
    if (len(string_with_numbers_spaced) > 0):
        raise Exception("Operação inválida.")
    
    # Verifica se começa com sinal de operação
    starts_with_signal = re.findall(pattern=r"^[+-]", string=operation)
    if (len(starts_with_signal) > 0):
        raise Exception("Operação inválida.")
    
    # Limpa espaços em branco
    string_clear = operation.replace(" ", "")

    result = eval(string_clear)
    print(result)
    return result

if __name__ == "__main__":
    check_sum()