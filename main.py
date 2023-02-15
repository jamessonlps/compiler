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
            if (current_exp_token == "+"):
                self.next = Token(token_type="plus", value=0)
                self.position += 1
                reading = False
            elif (current_exp_token == "-"):
                self.next = Token(token_type="minus", value=-1)
                self.position += 1
                reading = False
            elif (current_exp_token == " "):
                self.position += 1
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
        expression: str = ""
        while True:
            try:
                if (Parser.tokenizer.next.type == "int"):
                    if ((len(expression) > 0) and (expression[-1].isnumeric())):
                        raise Exception("Operação inválida.")
                    expression += str(Parser.tokenizer.next.value)
                elif (Parser.tokenizer.next.type == "plus"):
                    expression += "+"
                elif (Parser.tokenizer.next.type == "minus"):
                    expression += "-"
                else:
                    pass
                Parser.tokenizer.selectNext()
            except IndexError:
                break
        if not (expression[0].isnumeric()):
            raise Exception("Operação inválida.")
        result = eval(expression)
        print(result)
        return result

    @staticmethod
    def run(code) -> int:
        """
        Recebe o código fonte como argumento, inicializa 
        um objeto `Tokenizador`, posiciona no primeiro
        token e retorna o resultado do `parseExpression()`. 
        Esse método será chamado pelo `main()`. Ao final verificar
        se terminou de consumir (token é EOF).
        """
        Parser.tokenizer = Tokenizer(source=code)
        Parser.tokenizer.selectNext()
        return Parser.parseExpression()
        



if __name__ == "__main__":
    Parser.run(sys.argv[1])