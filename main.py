import re
import sys

class Token():
    def __init__(self, token_type: str, value: int) -> None:
        self.type = token_type
        self.value = value


class Tokenizer():
    def __init__(self, source: str, position: int = 0) -> None:
        self.source = source
        self.position = position
        self.next: Token = None
    
    def selectNext(self) -> None:
        """
        Lê o próximo token e atualiza o atributo `next`.
        """
        reading = True
        source_size = len(self.source)
        token = ""
        while reading:
            current_exp_token = self.source[self.position]
            # Sinal de adição
            if (current_exp_token == "+"):
                self.next = Token(token_type="plus", value=0)
                self.position += 1
                reading = False
            # Sinal de subtração
            elif (current_exp_token == "-"):
                self.next = Token(token_type="minus", value=-1)
                self.position += 1
                reading = False
            # Sinal de multiplicação
            elif (current_exp_token == "*"):
                self.next = Token(token_type="mult", value="*")
                self.position += 1
                reading = False
            # Sinal de divisão
            elif (current_exp_token == "/"):
                self.next = Token(token_type="div", value="//")
                self.position += 1
                reading = False
            # Espaço em branco (ignora)
            elif (current_exp_token in [" ", "\n", "\r", "\t"]):
                self.position += 1
            # Quando é número, verifica até chegar ao final do número
            elif (current_exp_token.isnumeric()):
                numeric_token = True
                while numeric_token:
                    token += current_exp_token
                    self.position += 1
                    if (self.position == source_size):
                        self.next = Token(token_type="int", value=int(token))
                        token = ""
                        numeric_token = False
                        reading = False
                    else:
                        current_exp_token = self.source[self.position]
                        if not (current_exp_token.isnumeric()):
                            numeric_token = False
                            reading = False
                            self.next = Token(token_type="int", value=int(token))
                            token = ""
            else:
                raise TypeError



class Parser():
    tokenizer: Tokenizer = None

    @staticmethod
    def parseExpression() -> int:
        """
        Consome os tokens do `tokenizer` e analisa se
        a sintaxe está aderente à gramática proposta.
        Retorna o resultado da expressão analisada.
        """
        expression_arr = []
        while True:
            try:
                # Se o token anterior é int, erro. Senão, acrescenta à exp.
                if (Parser.tokenizer.next.type == "int"):
                    if ((len(expression_arr) > 0) and (expression_arr[-1].isnumeric())):
                        raise Exception("Operação inválida.")
                    expression_arr.append(str(Parser.tokenizer.next.value))
                # Se o token é um sinal, adiciona à expressão
                elif (Parser.tokenizer.next.type == "plus"):
                    expression_arr.append("+")
                elif (Parser.tokenizer.next.type == "minus"):
                    expression_arr.append("-")
                # Se é outro sinal, manda pro parseTerm
                else:
                    expression_arr.append(Parser.parseTerm(number=expression_arr[-1], op=Parser.tokenizer.next.value))
                    expression_arr.pop(-2)
                # Avança o tokenizer
                Parser.tokenizer.selectNext()
            except IndexError:
                break
        if not (expression_arr[0].isnumeric()):
            raise Exception("Operação inválida.")
        expression = "".join(expression_arr)
        result = eval(expression)
        print(result)
        return result

    @staticmethod
    def parseTerm(number: int, op: str) -> str:
        """
        Trata o caso de multiplicação e divisão
        (prioridade sobre adição e subtração)
        """
        term: str = ""
        while True:
            try:
                Parser.tokenizer.selectNext()
                # Se o próximo é inteiro, faz a operação e retorna o resultado
                if (Parser.tokenizer.next.type == "int"):
                    term = str(number) + op + str(Parser.tokenizer.next.value)
                    return str(eval(term))
                else:
                    raise Exception("Erro no parseTerm")
            except IndexError:
                break

    @staticmethod
    def run(code) -> int:
        """
        Recebe o código fonte como argumento, inicializa 
        um objeto `Tokenizador`, posiciona no primeiro
        token e retorna o resultado do `parseExpression()`. 
        Esse método será chamado pelo `main()`. Ao final verificar
        se terminou de consumir (token é EOF).
        """
        code_processed = PrePro.filter(text=code)
        Parser.tokenizer = Tokenizer(source=code_processed)
        Parser.tokenizer.selectNext()
        return Parser.parseExpression()
        


class PrePro():
    @staticmethod
    def filter(text: str) -> str:
        return re.sub(pattern=r"#.*", repl="", string=text)


if __name__ == "__main__":
    Parser.run(sys.argv[1])