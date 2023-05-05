from abc import ABC, abstractmethod
from SymbolTable import symbol_table
from typing import Union
from _types import TypeValue


class Node(ABC):
  def __init__(self, value: Union[int, str], children) -> None:
    self.value: Union[int, str] = value
    self.children: list[Node] = children

  @abstractmethod
  def evaluate(self) -> TypeValue:
    ...


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
  
  def evaluate(self) -> None:
    symbol_table.setter(
      key=self.children[0].value, 
      value=self.children[1].evaluate()
    )


class PrintlnNode(Node):
  def __init__(self) -> None:
    super().__init__(value=0, children=[])
  
  def evaluate(self) -> None:
    print(self.children[0].evaluate().value)


class IdentifierNode(Node):
  def __init__(self, value: str) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self) -> str:
    return symbol_table.getter(self.value)


class ReadlineNode(Node):
  def __init__(self) -> None:
    super().__init__(value="read", children=[])
  
  def evaluate(self) -> int:
    return TypeValue("Int", int(input(""))) 


class WhileNode(Node):
  def __init__(self) -> None:
    super().__init__("while", children=[])
  
  def evaluate(self):
    while (self.children[0].evaluate().value == 1):
      self.children[1].evaluate()
    

class ConditionalNode(Node):
  def __init__(self, value: str) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self):
    # Após o else não há nenhuma condicional
    if self.value == "else":
      self.children[0].evaluate()
    # Se for if, resolve se a condição em children[0] for True
    elif (self.children[0].evaluate().value == 1):
      self.children[1].evaluate()
    # Se a anterior é False e há um else, resolve em children[2]
    elif (len(self.children) >= 3):
      self.children[2].evaluate()


class BinUp(Node):
  def __init__(self, value, children) -> None:
    super().__init__(value=value, children=children)

  def evaluate(self) -> TypeValue:
    type_left = self.children[0].evaluate().type
    type_right = self.children[1].evaluate().type

    if type_left != type_right:
      raise SyntaxError(f"You cannot perform operations with different types: {type_left} and {type_right}")
    
    left = self.children[0].evaluate().value
    right = self.children[1].evaluate().value
    
    if self.value == "+":
      return TypeValue("Int", left + right)
    elif self.value == "-":
      return TypeValue("Int", left - right)
    elif self.value == "*":
      return TypeValue("Int", left * right)
    elif (self.value == "/"):
      return TypeValue("Int", left // right)
    elif (self.value == "=="):
      result = 1 if left == right else 0
      return TypeValue("Int", result)
    elif (self.value == ">"):
      result = 1 if left > right else 0
      return TypeValue("Int", result)
    elif (self.value == "<"):
      result = 1 if left < right else 0
      return TypeValue("Int", result)
    elif (self.value == "&&"):
      return TypeValue("Int", left and right)
    elif (self.value == "||"):
      return TypeValue("Int", left or right)
    elif (self.value == "."):
      if not isinstance(left, str) or not isinstance(right, str):
        raise SyntaxError(f"Cannot concatenate non-string values: {type_left} and {type_right}")
      return TypeValue("String", str(left) + str(right))
    raise SyntaxError("Cannot evaluate a bin operation:", left, self.value, right)
  


class UnOp(Node):
  def __init__(self, value, children) -> None:
    super().__init__(value, children)

  def evaluate(self) -> TypeValue:
    if (self.value == "+"):
      return self.children[0].evaluate()
    elif (self.value == "-"):
      return -self.children[0].evaluate()
    elif (self.value == "!"):
      return not self.children[0].evaluate()
    else:
      raise SyntaxError("Invalid unary operation: value = ", self.value)



class IntVal(Node):
  def __init__(self, value: int) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self) -> TypeValue:
    return TypeValue("Int", self.value)


class StrVal(Node):
  def __init__(self, value: str) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self) -> TypeValue:
    return TypeValue("String", self.value)


class NoOp(Node):
  def __init__(self) -> None:
    super().__init__(value=None, children=None)

  def evaluate(self) -> int:
    pass


class VariableDeclarationNode(Node):
  """
  @param `value`: type of the variable
  """
  def __init__(self, value: str) -> None:
    super().__init__(value=value, children=[])
  
  def evaluate(self) -> None:
    if len(self.children) > 1:
      item = TypeValue(self.value, self.children[1].evaluate().value)
      symbol_table.create(self.children[0].value, item)
    else:
      if self.value == "Int":
        item = TypeValue(self.value, 0)
      elif self.value == "String":
        item = TypeValue(self.value, "")
      else:
        raise SyntaxError(f"Invalid type of variable declaration: {self.value} :: {self.children[0].value}")
      symbol_table.create(self.children[0].value, item)