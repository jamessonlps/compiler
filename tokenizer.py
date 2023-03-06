from tokens import *

class Tokenizer():
    def __init__(self, source: str, position: int = 0) -> None:
        self.source = source
        self.position = position
        self.next: Token = None
    
    def selectNext(self) -> None:
        source_size = len(self.source)
        current_token = self.source[self.position]

        if current_token == "+":
            self.next = PlusToken()
            self.position += 1
        elif current_token == "-":
            self.next = MinusToken()
            self.position += 1
        elif current_token == "*":
            self.next = MultiplicationToken()
            self.position += 1
        elif current_token == "/":
            self.next == DivisionToken()
            self.position += 1
        elif current_token == "(":
            self.next = ParenthesisToken(parenthesis_type="start")
            self.position += 1
        elif current_token == ")":
            self.next = ParenthesisToken(parenthesis_type="end")
            self.position += 1
        elif current_token.isdigit():
            pos = self.position
            number_str = ""
            while (current_token.isdigit() and pos < source_size):
                number_str += current_token
                pos += 1
                self.position += 1
                if (pos < source_size):
                    current_token = self.source[self.position]
            self.next = NumberToken(value=int(number_str))
        # White space
        elif current_token.isspace():
            pos = self.position
            while (current_token.isspace() and pos < source_size):
                # Update read position and get next token
                pos += 1
                self.position += 1
                if pos < source_size:
                    current_token = self.source[self.position]
        else:
            raise TypeError
