from tokens import *

class Tokenizer():
    def __init__(self, source: str, position: int = 0) -> None:
        self.source = source
        self.position = position
        self.next: Token = None


    def selectNext(self) -> None:
        """
        Set the next token to the `next` param.
        """
        source_size = len(self.source)
        reading = True
        
        while reading:
            current_token = self.source[self.position]
            print("Token atual:", current_token)
            if current_token == "+":
                self.next = PlusToken()
                self.position += 1
                reading = False
            elif current_token == "-":
                self.next = MinusToken()
                self.position += 1
                reading = False
            elif current_token == "*":
                self.next = MultiplicationToken()
                self.position += 1
                reading = False
            elif current_token == "/":
                self.next == DivisionToken()
                self.position += 1
                reading = False
            elif current_token == "(":
                self.next = LeftParenthesisToken()
                self.position += 1
                reading = False
            elif current_token == ")":
                self.next = RightParenthesisToken()
                self.position += 1
                reading = False
            elif current_token == "\0":
                self.next = EndOfFileToken()
                reading = False
            # Number case
            elif current_token.isdigit():
                number_str = ""
                while (current_token.isdigit() and self.position < source_size):
                    number_str += current_token
                    self.position += 1
                    if (self.position < source_size):
                        current_token = self.source[self.position]
                self.next = NumberToken(int(number_str))
                reading = False
            # White space case
            elif current_token.isspace():
                self.position += 1
            else:
                raise TypeError(f"Invalid Token: {current_token}")
