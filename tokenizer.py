from tokens import *


reserveds = {
    "println": PrintlnToken,
    "readline": ReadlineToken,
    "while": WhileToken,
    "if": IfToken,
    "else": ElseToken,
    "end": EndIfToken,
    "Int": IntegerTypeToken,
    "String": StringTypeToken,
    "function": FunctionDeclarationToken,
    "return": ReturnToken,
}


class Tokenizer():
    def __init__(self, source: str, position: int = 0) -> None:
        self.source = source
        self.position = position
        self.next: Token = None
        self._source_size = len(source)
    

    def _get_number_token(self, current_token: str) -> None:
        number_string = ""
        token = current_token
        while ((token.isdigit()) and (self.position < self._source_size)):
            number_string += token
            self.position += 1
            if self.position < self._source_size:
                token = self.source[self.position]
        self.next = NumberToken(int(number_string))


    def selectNext(self) -> None:
        self.next, self.position = self.see_next_token()


    def see_next_token(self) -> tuple[Token, int]:
        """
        Set the next token to the `next` param.
        """
        current_token = self.source[self.position]

        position = self.position
        next_token = self.next
        
        # Jump all wihte spaces before get next valid token
        if (current_token.isspace() and current_token != "\n"):
            while ((current_token.isspace()) and (position < self._source_size) and (current_token != "\n")):
                position += 1
                if position < self._source_size:
                    current_token = self.source[position]

        # Get identifier token
        if (current_token.isalpha()):
            identifier_str = ""
            while (current_token.isalnum() or current_token == "_"):
                identifier_str += current_token
                position += 1
                if position < self._source_size:
                    current_token = self.source[position]

            if identifier_str in reserveds.keys():
                next_token = reserveds[identifier_str]()
            else:
                next_token = IdentifierToken(value=identifier_str)

        # Get string token
        elif current_token == "\"":
            position += 1
            current_token = self.source[position]
            string = ""
            while (current_token != "\""):
                string += current_token
                position += 1
                current_token = self.source[position]
                if position == self._source_size:
                    raise TypeError("Invalid string. Did you forget to close it?")
            next_token = StringToken(value=string)
            position += 1
        
        # Get number token
        elif current_token.isdigit():
            number_string = ""
            while ((current_token.isdigit()) and (position < self._source_size)):
                number_string += current_token
                position += 1
                if position < self._source_size:
                    current_token = self.source[position]
            next_token = NumberToken(int(number_string))


        elif current_token == "&":
            position += 1
            current_token = self.source[position]
            if current_token == "&":
                next_token = LogicAndToken()
                position += 1
            else:
                raise TypeError("Invalid token. Did you mean '&&'?")
        
        elif current_token == ":":
            position += 1
            current_token = self.source[position]
            if current_token == ":":
                next_token = VariableDeclarationToken()
                position += 1
            else:
                raise TypeError("Invalid token. Did you mean '::'?")
        
        elif current_token == "|":
            position += 1
            current_token = self.source[position]
            if current_token == "|":
                next_token = LogicOrToken()
                position += 1
            else:
                raise TypeError("Invalid token. Did you mean '||'?")
        
        elif current_token == "=":
            position += 1
            current_token = self.source[position]
            if current_token == "=":
                next_token = CompareEqualToToken()
                position += 1
            elif current_token.isspace():
                next_token = EqualsToken()
                position += 1
            else:
                raise TypeError("Invalid token. Token received after '=': ", current_token)
        
        elif current_token == "\n":
            next_token = BreakLineToken()
            position += 1
        
        elif current_token == "+":
            next_token = PlusToken()
            position += 1
        
        elif current_token == ".":
            next_token = DotToken()
            position += 1
        
        elif current_token == ",":
            next_token = CommaToken()
            position += 1
        
        elif current_token == "-":
            next_token = MinusToken()
            position += 1
        
        elif current_token == "*":
            next_token = MultiplicationToken()
            position += 1
        
        elif current_token == "/":
            next_token = DivisionToken()
            position += 1
        
        elif current_token == "!":
            next_token = DenialToken()
            position += 1
        
        elif current_token == "<":
            next_token = CompareLessThenToken()
            position += 1
        
        elif current_token == ">":
            next_token = CompareGreaterThenToken()
            position += 1
        
        elif current_token == "(":
            next_token = LeftParenthesisToken()
            position += 1
        
        elif current_token == ")":
            next_token = RightParenthesisToken()
            position += 1
        
        elif current_token == "\0":
            next_token = EndOfFileToken()
        
        else:
            raise TypeError(f"Unexpected or invalid token: {current_token}")
        
        return next_token, position
