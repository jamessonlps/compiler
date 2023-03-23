from abc import ABC, abstractmethod
from SymbolTable import symbol_table
from typing import Union


class Node(ABC):
  def __init__(self, value: Union[int, str], children) -> None:
    self.value: Union[int, str] = value
    self.children: list[Node] = children

  @abstractmethod
  def evaluate(self) -> int | None:
    return


class BlockNode(Node):
  def __init__(self) -> None:
    super().__init__(value=0, children=[])
  
  def evaluate(self) -> None:
    for child in self.children:
      if not isinstance(child, NoOp):
        child.evaluate()


class AssignmentNode(Node):
  def __init__(self) -> None:
    super().__init__(value=0, children=[])
  
  def evaluate(self):
    symbol_table.setter(self.children[0].value, self.children[1].evaluate())


class PrintlnNode(Node):
  def __init__(self) -> None:
    super().__init__(value=0, children=[])
  
  def evaluate(self) -> None:
    print(self.children[0].evaluate())


class IdentifierNode(Node):
  def __init__(self, value: str) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self) -> str:
    return symbol_table.getter(self.value)


class BinUp(Node):
  def __init__(self, value, children) -> None:
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
  def __init__(self, value: int) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self) -> int:
    return self.value



class NoOp(Node):
  def __init__(self, value, children) -> None:
    super().__init__(value, children)

  def evaluate(self) -> int:
    pass