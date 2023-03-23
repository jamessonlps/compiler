from abc import ABC, abstractproperty
from typing import Union


class Token(ABC):
    def __init__(self, value: Union[int, str]) -> None:
        self._value = value
    
    @abstractproperty
    def value(self):
        return self._value



# ------- Token que representa números -------
class NumberToken(Token):
    def __init__(self, value: int) -> None:
        super().__init__(value)

    @property
    def value(self) -> int:
        return self._value



# ------- Token que representa sinais de operação -------
class PlusToken(Token):
    def __init__(self) -> None:
        super().__init__("+")
    
    @property
    def value(self) -> str:
        return self._value



class MinusToken(Token):
    def __init__(self) -> None:
        super().__init__("-")
    
    @property
    def value(self) -> str:
        return self._value



class MultiplicationToken(Token):
    def __init__(self) -> None:
        super().__init__("*")
    
    @property
    def value(self) -> str:
        return self._value



class DivisionToken(Token):
    def __init__(self) -> None:
        super().__init__("/")
    
    @property
    def value(self) -> str:
        return self._value


class EqualsToken(Token):
    def __init__(self) -> None:
        super().__init__("=")
    
    @property
    def value(self) -> str:
        return self._value
    

class BreakLineToken(Token):
    def __init__(self) -> None:
        super().__init__("\n")
    
    @property
    def value(self) -> str:
        return self._value


class IdentifierToken(Token):
    def __init__(self, value: str) -> None:
        super().__init__(value)
    
    @property
    def value(self) -> str:
        return self._value



# ------- Tokens de outros sinais -------
class ParenthesisToken(Token):
    def __init__(self) -> None:
        super().__init__(0)

    @property
    def value(self) -> str:
        return "Parenthesis"


class LeftParenthesisToken(ParenthesisToken):
    def __init__(self) -> None:
        super().__init__()
    
    @property
    def value(self) -> str:
        return "("



class RightParenthesisToken(ParenthesisToken):
    def __init__(self) -> None:
        super().__init__()
    
    @property
    def value(self) -> str:
        return ")"


class PrintlnToken(Token):
    def __init__(self) -> None:
        super().__init__("println")
    
    @property
    def value(self) -> str:
        return self._value
    


# ------- Token para o final do arquivo (EOF) -------
class EndOfFileToken(Token):
    def __init__(self) -> None:
        super().__init__("\0")
    
    @property
    def value(self) -> str:
        return self._value