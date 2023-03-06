
from typing import Union


class Token():
    def __init__(self, value: Union[int, str]) -> None:
        self.value = value

# ------- Token que representa números -------
class NumberToken(Token):
    def __init__(self, value: int) -> None:
        super().__init__(value=value)

    @property
    def value(self) -> int:
        return self.value

    @property
    def type(self) -> str:
        return "number" 


# ------- Token que representa sinais de operação -------
class PlusToken(Token):
    def __init__(self) -> None:
        super().__init__(0)
    
    @property
    def type(self) -> str:
        return "+"


class MinusToken(Token):
    def __init__(self) -> None:
        super().__init__(0)
    
    @property
    def type(self) -> str:
        return "-"


class MultiplicationToken(Token):
    def __init__(self) -> None:
        super().__init__(0)
    
    @property
    def type(self) -> str:
        return "*"


class DivisionToken(Token):
    def __init__(self) -> None:
        super().__init__(0)
    
    @property
    def type(self) -> str:
        return "/"


# ------- Tokens de outros sinais -------
class ParenthesisToken(Token):
    def __init__(self, parenthesis_type: str) -> None:
        super().__init__(0)
        if parenthesis_type not in ["start", "end"]:
            raise Exception("Parenthesis type must be 'start' or 'end'")
        self.parenthesis_type = parenthesis_type

    @property
    def type(self) -> str:
        if self.parenthesis_type == "start":
            return "("
        return ")"


# ------- Tokens para o final do arquivo -------
class EndOfFileToken(Token):
    def __init__(self) -> None:
        super().__init__(0)
    
    @property
    def type(self) -> str:
        return "\0"