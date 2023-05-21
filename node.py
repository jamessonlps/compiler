from abc import ABC, abstractmethod
from SymbolTable import SymbolTable
from FunctionTable import function_table
from typing import Union, List
from _types import TypeValue


class Node(ABC):
  def __init__(self, value: Union[int, str], children) -> None:
    self.value: Union[int, str] = value
    self.children: List[Node] = children

  @abstractmethod
  def evaluate(self, symbol_table: SymbolTable) -> TypeValue:
    ...


class BlockNode(Node):
  def __init__(self, value="block") -> None:
    super().__init__(value=value, children=[])
  
  def evaluate(self, symbol_table) -> None:
    for child in self.children:
      if not isinstance(child, NoOp) and child is not None:
        result = child.evaluate(symbol_table)
    
    if self.value != "root":
      return result


class AssignmentNode(Node):
  """
  @param `children`:
    [0] -> Identifier\n
    [1] -> RelExpression
  """
  def __init__(self, children: List[Node] = []) -> None:
    super().__init__(value=0, children=children)
  
  def evaluate(self, symbol_table) -> None:
    symbol_table.setter(
      key=self.children[0].value, 
      value=self.children[1].evaluate(symbol_table)
    )


class PrintlnNode(Node):
  def __init__(self) -> None:
    super().__init__(value=0, children=[])
  
  def evaluate(self, symbol_table) -> None:
    print(self.children[0].evaluate(symbol_table).value)


class IdentifierNode(Node):
  """
  @param `value`: name of the variable or function
  """
  def __init__(self, value: str) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self, symbol_table) -> TypeValue:
    return symbol_table.getter(self.value)


class ReadlineNode(Node):
  def __init__(self) -> None:
    super().__init__(value="read", children=[])
  
  def evaluate(self, symbol_table) -> TypeValue:
    return TypeValue("Int", int(input(""))) 


class WhileNode(Node):
  def __init__(self) -> None:
    super().__init__("while", children=[])
  
  def evaluate(self, symbol_table):
    while (self.children[0].evaluate(symbol_table).value == 1):
      self.children[1].evaluate(symbol_table)
    

class ConditionalNode(Node):
  def __init__(self, value: str) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self, symbol_table: SymbolTable):
    # Após o else não há nenhuma condicional
    if self.value == "else":
      self.children[0].evaluate(symbol_table)
    # Se for if, resolve se a condição em children[0] for True
    elif (self.children[0].evaluate(symbol_table).value == 1):
      self.children[1].evaluate(symbol_table)
    # Se a anterior é False e há um else, resolve em children[2]
    elif (len(self.children) >= 3):
      self.children[2].evaluate(symbol_table)


class BinUp(Node):
  def __init__(self, value, children) -> None:
    super().__init__(value=value, children=children)

  def evaluate_int(self, left, right) -> TypeValue:
    """
    Evaluate a binary operation between two integers
    """
    if self.value == "+":
      return TypeValue("Int", left + right)
    
    elif self.value == "-":
      return TypeValue("Int", left - right)
    
    elif self.value == "*":
      return TypeValue("Int", left * right)
    
    elif (self.value == "/"):
      return TypeValue("Int", left // right)
  
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
    
    elif (self.value == "=="):
      result = 1 if left == right else 0
      return TypeValue("Int", result)
    
    elif (self.value == "."):
      return TypeValue("String", str(left) + str(right))
    
  def evaluate_str(self, left, right) -> TypeValue:
    """
    Evaluate a binary operation between two strings
    """
    if (self.value == "=="):
      result = 1 if left == right else 0
      return TypeValue("Int", result)
    
    elif (self.value == ">"):
      result = 1 if left > right else 0
      return TypeValue("Int", result)
    
    elif (self.value == "<"):
      result = 1 if left < right else 0
      return TypeValue("Int", result)
    
    elif (self.value == "."):
      return TypeValue("String", str(left) + str(right))

  def evaluate_any(self, left, right) -> TypeValue:
    """
    Evaluate a binary operation between two different types
    """
    if (self.value == "."):
      return TypeValue("String", str(left) + str(right))
    elif (self.value == "=="):
      result = 1 if left == right else 0
      return TypeValue("Int", result)
    raise SyntaxError(f"Invalid operation: {left} {self.value} {right}")

  def evaluate(self, symbol_table) -> TypeValue:
    type_left, left = self.children[0].evaluate(symbol_table).instance
    type_right, right = self.children[1].evaluate(symbol_table).instance

    # Operações entre inteiros
    if ((type_left == type_right) and type_left == "Int"):
      return self.evaluate_int(left, right)
    
    # Operações entre strings
    elif ((type_left == type_right) and type_left == "String"):
      return self.evaluate_str(left, right)
    
    # Operação entre qualquer tipo
    elif (type_left != type_right):
      return self.evaluate_any(left, right)
    
    raise SyntaxError(f"Cannot evaluate a bin operation: {left} {self.value} {right}")
  


class UnOp(Node):
  def __init__(self, value, children) -> None:
    super().__init__(value, children)

  def evaluate(self, symbol_table) -> TypeValue:
    if (self.value == "+"):
      return TypeValue("Int", self.children[0].evaluate(symbol_table).value)
    elif (self.value == "-"):
      return TypeValue("Int", -self.children[0].evaluate(symbol_table).value)
    elif (self.value == "!"):
      return TypeValue("Int", not self.children[0].evaluate(symbol_table).value)
    else:
      raise SyntaxError(f"Invalid unary operation: value = {self.value} :: children = {self.children[0]}")



class IntVal(Node):
  def __init__(self, value: int) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self, symbol_table) -> TypeValue:
    return TypeValue("Int", self.value)


class StrVal(Node):
  def __init__(self, value: str) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self, symbol_table) -> TypeValue:
    return TypeValue("String", self.value)


class NoOp(Node):
  def __init__(self) -> None:
    super().__init__(value=None, children=None)

  def evaluate(self, symbol_table) -> int:
    pass


class VariableDeclarationNode(Node):
  """
  @param `value`: type of the variable
  @param `children`: 
    [0] -> name of the variable (`Identifier`)\n
    [1] -> value of the variable
  """
  def __init__(self, value: str, children=[]) -> None:
    super().__init__(value=value, children=children)
  
  def evaluate(self, symbol_table) -> None:
    if len(self.children) > 1:
      item = TypeValue(self.value, self.children[1].evaluate(symbol_table).value)
      symbol_table.create(self.children[0].value, item)
    else:
      if self.value == "Int":
        item = TypeValue(self.value, 0)
      elif self.value == "String":
        item = TypeValue(self.value, "")
      else:
        raise SyntaxError(f"Invalid type of variable declaration: {self.value} :: {self.children[0].value}")
      symbol_table.create(self.children[0].value, item)


class FunctionDeclarationNode(Node):
  """
  It's responsible for creating a function in the function table.

  @param `value`: return type of the function
  @param `children`:
    [0]   -> name of the function (`Identifier`)\n
    [...] -> parameters of the function (`VariableDeclarationNode`)\n
    [-1]  -> body of the function (`Block`)
  """
  def __init__(self, value: str, children: List[Node]) -> None:
    super().__init__(value=value, children=children)
    self.num_params = len(children) - 2
    self.return_type = value
  
  def evaluate(self, symbol_table) -> None:
    function_name = self.children[0].value
    function_table.create(function_name, self)


class ReturnNode(Node):
  """
  @param `children`:
    [0] -> value to return (rel_expression)
  """
  def __init__(self, children: List[Node]) -> None:
    super().__init__(value="return", children=children)
  
  def evaluate(self, symbol_table) -> TypeValue:
    return self.children[0].evaluate(symbol_table)


class FunctionCallNode(Node):
  """
  @param `value`: name of the function
  @param `children`: parameters of the function (Identifier, IntVal, StrVal, BinOp, UnOp)
  """
  def __init__(self, value: str, children: List[Node]) -> None:
    super().__init__(value=value, children=children)

  def evaluate(self, symbol_table) -> TypeValue:
    function_dec = function_table.getter(self.value)

    if (function_dec.num_params != len(self.children)):
      raise SyntaxError(f"Number of params expected: {function_dec.num_params}. Received: {len(self.children)}")
    
    function_symbol_table = SymbolTable(name=self.value)
    
    for i in range(len(self.children)):
      type_expected = function_dec.children[i+1].value
      type_received, arg_received = self.children[i].evaluate(symbol_table).instance
      
      if type_expected != type_received:
        raise SyntaxError(f"Type param mismatch on function '{self.value}': {type_expected} != {type_received}")
      
      function_dec.children[i+1].evaluate(function_symbol_table)
      function_symbol_table.setter(function_dec.children[i+1].children[0].value, TypeValue(type_expected, arg_received))
  
    return_value: TypeValue = function_dec.children[-1].evaluate(function_symbol_table)

    if return_value.type != function_dec.return_type:
      raise SyntaxError(f"Type mismatch on function '{self.value}' return type: {function_dec.return_type} != {return_value.type}")
    
    return return_value