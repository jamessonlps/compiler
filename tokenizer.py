from tokens import *


reserveds = {
    "println": PrintlnToken
}


class Tokenizer():
    def __init__(self, source: str, position: int = 0) -> None:
        self.source = source
        self.position = position
        self.next: Token = None
        self._source_size = len(source)
    

    def _jump_white_spaces(self, current_token: str) -> str:
        token = current_token
        while ((token.isspace()) and (self.position < self._source_size) and (token != "\n")):
            self.position += 1
            if self.position < self._source_size:
                token = self.source[self.position]
        return token
    

    def _get_number_token(self, current_token: str) -> None:
        number_string = ""
        token = current_token
        while ((token.isdigit()) and (self.position < self._source_size)):
            number_string += token
            self.position += 1
            if self.position < self._source_size:
                token = self.source[self.position]
        self.next = NumberToken(int(number_string))


    def _get_identifier_token(self, current_token: str) -> None:
        identifier_str = ""
        token = current_token
        while (token.isalnum() or token == "_"):
            identifier_str += token
            self.position += 1
            if self.position < self._source_size:
                token = self.source[self.position]

        if identifier_str in reserveds.keys():
            self.next = reserveds[identifier_str]()
        else:
            self.next = IdentifierToken(value=identifier_str)


    def selectNext(self) -> None:
        """
        Set the next token to the `next` param.
        """
        current_token = self.source[self.position]
        
        # Jump all wihte spaces before get next valid token
        if (current_token.isspace() and current_token != "\n"):
            current_token = self._jump_white_spaces(current_token=current_token)
        
        if (current_token.isalpha()):
            self._get_identifier_token(current_token=current_token)
        
        elif current_token == "\n":
            self.next = BreakLineToken()
            self.position += 1
        
        elif current_token.isdigit():
            self._get_number_token(current_token=current_token)
        
        elif current_token == "=":
            self.next = EqualsToken()
            self.position += 1
        
        
        elif current_token == "+":
            self.next = PlusToken()
            self.position += 1
        
        elif current_token == "-":
            self.next = MinusToken()
            self.position += 1
        
        elif current_token == "*":
            self.next = MultiplicationToken()
            self.position += 1
        
        elif current_token == "/":
            self.next = DivisionToken()
            self.position += 1
        
        elif current_token == "(":
            self.next = LeftParenthesisToken()
            self.position += 1
        
        elif current_token == ")":
            self.next = RightParenthesisToken()
            self.position += 1
        
        elif current_token == "\0":
            self.next = EndOfFileToken()
        
        else:
            raise TypeError(f"Unexpected or invalid token: {current_token}")
