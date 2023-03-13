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
  def __init__(self, value, children) -> None:
    super().__init__(value=value, children=children)

  def evaluate(self) -> int:
    left = self.children[0].evaluate()
    right = self.children[1].evaluate()
    if (self.value in ["+", "-", "*"]):
      return int(eval(f"{left} {self.value} {right}"))
    elif (self.value == "/"):
      return left // right
    raise SyntaxError("Cannot evaluate a bin operation:", left, self.value, right)
  


class UnOp(Node):
  def __init__(self, value, children) -> None:
    super().__init__(value, children)

  def evaluate(self) -> int:
    return self.children[0].evaluate()



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