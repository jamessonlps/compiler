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


class StringToken(Token):
    def __init__(self, value: str) -> None:
        super().__init__(value)
    
    @property
    def value(self) -> str:
        return self._value


class VariableDeclarationToken(Token):
    def __init__(self) -> None:
        super().__init__("::")
    
    @property
    def value(self) -> str:
        return self._value


class TypeVariableToken(Token):
    def __init__(self, value: str) -> None:
        super().__init__(value)
    
    @property
    def value(self) -> str:
        return self._value


class IntegerTypeToken(TypeVariableToken):
    def __init__(self) -> None:
        super().__init__("Int")
    
    @property
    def value(self) -> str:
        return self._value
    

class StringTypeToken(TypeVariableToken):
    def __init__(self) -> None:
        super().__init__("String")
    
    @property
    def value(self) -> str:
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


class DenialToken(Token):
    def __init__(self) -> None:
        super().__init__("!")
    
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


class CommaToken(Token):
    def __init__(self) -> None:
        super().__init__(",")

    @property
    def value(self) -> str:
        return self._value


class IdentifierToken(Token):
    def __init__(self, value: str) -> None:
        super().__init__(value)
    
    @property
    def value(self) -> str:
        return self._value


class DotToken(Token):
    def __init__(self) -> None:
        super().__init__(".")
    
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


class CompareEqualToToken(Token):
    def __init__(self) -> None:
        super().__init__("==")
    
    @property
    def value(self) -> str:
        return self._value


class CompareLessThenToken(Token):
    def __init__(self) -> None:
        super().__init__("<")
    
    @property
    def value(self) -> str:
        return self._value


class CompareGreaterThenToken(Token):
    def __init__(self) -> None:
        super().__init__(">")
    
    @property
    def value(self) -> str:
        return self._value


class LogicOrToken(Token):
    def __init__(self) -> None:
        super().__init__("||")
    
    @property
    def value(self) -> str:
        return self._value


class LogicAndToken(Token):
    def __init__(self) -> None:
        super().__init__("&&")
    
    @property
    def value(self) -> str:
        return self._value


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
    

class ReadlineToken(Token):
    def __init__(self) -> None:
        return super().__init__("readline")

    @property
    def value(self) -> str:
        return self._value


class FunctionDeclarationToken(Token):
    def __init__(self) -> None:
        return super().__init__("function")

    @property
    def value(self) -> str:
        return self._value


class ReturnToken(Token):
    def __init__(self) -> None:
        return super().__init__("return")

    @property
    def value(self) -> str:
        return self._value


# ------- Tokens para loopings e condicionais -------
class WhileToken(Token):
    def __init__(self) -> None:
        return super().__init__("while")

    @property
    def value(self) -> str:
        return self._value


class IfToken(Token):
    def __init__(self) -> None:
        return super().__init__("if")

    @property
    def value(self) -> str:
        return self._value


class ElseToken(Token):
    def __init__(self) -> None:
        return super().__init__("else")

    @property
    def value(self) -> str:
        return self._value


class EndIfToken(Token):
    def __init__(self) -> None:
        return super().__init__("end")

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