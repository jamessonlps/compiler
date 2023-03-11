
from typing import Union


class Token():
    def __init__(self, value: Union[int, str]) -> None:
        self._value = value



# ------- Token que representa números -------
class NumberToken(Token):
    def __init__(self, value: int) -> None:
        super().__init__(value)

    @property
    def value(self) -> int:
        return self._value
    
    @value.setter
    def value(self, value) -> int:
        self._value = value

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
    def __init__(self) -> None:
        super().__init__(0)

    @property
    def type(self) -> str:
        return "Parenthesis"


class LeftParenthesisToken(ParenthesisToken):
    def __init__(self) -> None:
        super().__init__()
    
    @property
    def type(self) -> str:
        return "("



class RightParenthesisToken(ParenthesisToken):
    def __init__(self) -> None:
        super().__init__()
    
    @property
    def type(self) -> str:
        return ")"



# ------- Token para o final do arquivo (EOF) -------
class EndOfFileToken(Token):
    def __init__(self) -> None:
        super().__init__(0)
    
    @property
    def type(self) -> str:
        return "\0"