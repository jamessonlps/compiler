from abc import ABC, abstractmethod
from typing import Union


class Node(ABC):
  def __init__(self, value: Union[int, str], children) -> None:
    self.value: Union[int, str] = value
    self.children: list[Node] = children

  @abstractmethod
  def evaluate(self) -> int:
    pass



class BinUp(Node):
  def __init__(self, value, children: list[Node] = []) -> None:
    super().__init__(value=value, children=children)

  def evaluate(self) -> int:
    left = self.children[0].evaluate()
    right = self.children[1].evaluate()
    if self.value == "+":
      return left + right
    elif self.value == "-":
      return left - right
    elif self.value == "*":
      return left * right
    elif (self.value == "/"):
      return left // right
    raise SyntaxError("Cannot evaluate a bin operation:", left, self.value, right)
  


class UnOp(Node):
  def __init__(self, value, children) -> None:
    super().__init__(value, children)

  def evaluate(self) -> int:
    if (self.value == "+"):
      return self.children[0].evaluate()
    elif (self.value == "-"):
      return -self.children[0].evaluate()
    else:
      raise SyntaxError("Invalid unary operation: value = ", self.value)



class IntVal(Node):
  def __init__(self, value: Union[int, str]) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self) -> int:
    return self.value



class NoOp(Node):
  def __init__(self, value, children) -> None:
    super().__init__(value, children)

  def evaluate(self) -> int:
    pass