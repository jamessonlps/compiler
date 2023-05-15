from abc import ABC, abstractmethod
from SymbolTable import symbol_table
from typing import Union
from _types import TypeValue

class IdGenerator:
  counter = 0


class Node(ABC):
  def __init__(self, value: Union[int, str], children) -> None:
    self.value: Union[int, str] = value
    self.children: list[Node] = children
    self.id = IdGenerator.counter
    IdGenerator.counter += 1

  @abstractmethod
  def evaluate(self) -> Union[str, None]:
    ...


class BlockNode(Node):
  def __init__(self) -> None:
    super().__init__(value=0, children=[])
  
  def evaluate(self) -> str:
    block = ""
    for child in self.children:
      if not isinstance(child, NoOp):
        block += child.evaluate()
    return block


class AssignmentNode(Node):
  """
  @param `value`: 
  @param `children`: [0] = Identifier, [1] = RelExpression
  """
  def __init__(self) -> None:
    super().__init__(value=0, children=[])
  
  def evaluate(self) -> str:
    if isinstance(self.children[1], (IntVal, AssignmentNode)):
      return f"""
        ; Assignment: {self.children[0].value}
        MOV EBX, {self.children[1].evaluate()}
        MOV {self.children[0].evaluate()}, EBX
      """
    else:
      return f"""
        ; Assignment: {self.children[0].value}
        {self.children[1].evaluate()}
        MOV {self.children[0].evaluate()}, EBX
      """


class PrintlnNode(Node):
  """
  @param `value`: value to be printed (`rel_expression`)
  @param `children`: [0] = rel_expression
  """
  def __init__(self) -> None:
    super().__init__(value=0, children=[])
  
  def evaluate(self) -> str:
    if isinstance(self.children[0], (IntVal, IdentifierNode)):
      return f"""
        ; Println(Identifier | IntVal)
        MOV EBX, {self.children[0].evaluate()}
        PUSH EBX
        CALL print
        POP EBX
      """
    else:
      return f"""
        ; Println(RelExpression)
        {self.children[0].evaluate()}
        PUSH EBX
        CALL print
        POP EBX
      """


class IdentifierNode(Node):
  def __init__(self, value: str) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self) -> str:
    return f"[EBP-{symbol_table.getter(self.value)}]"


class ReadlineNode(Node):
  def __init__(self) -> None:
    super().__init__(value="read", children=[])
  
  def evaluate(self) -> TypeValue:
    return TypeValue("Int", int(input(""))) 


class WhileNode(Node):
  """
  @param `value`: "while"
  @param `children`: [0] = BinOp, [1]+ = Block
  """
  def __init__(self) -> None:
    super().__init__("while", children=[])
  
  def evaluate(self) -> str:
    return f"""
      ; While
      LOOP_{self.id}:
      {self.children[0].evaluate()}
      CMP EBX, False
      JE EXIT_{self.id}
      {self.children[1].evaluate()}
      JMP LOOP_{self.id}
      EXIT_{self.id}:
    """
    

class ConditionalNode(Node):
  """
  @param `value`: "if" or "else"
  @param `children`: [0] = BinOp, [1] = Block, [2] = Block (else)
  """
  def __init__(self, value: str) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self) -> str:
    # After else, there is no more children
    if self.value == "else":
      else_block = ""
      for child in self.children:
        if not isinstance(child, NoOp):
          else_block += child.evaluate()
      return else_block
    elif len(self.children) > 2:
      return f"""
        ; if/else => if
        CONDITION_IF_{self.id}:
        {self.children[0].evaluate()}
        CMP EBX, False
        JE CONDITION_ELSE_{self.children[2].id}
        {self.children[1].evaluate()}
        JMP EXIT_IF_{self.id}
        ; if/else => else
        CONDITION_ELSE_{self.children[2].id}:
        {self.children[2].evaluate()}
        EXIT_IF_{self.id}:
      """
    else:
      return f"""
        ; if
        CONDITION_{self.id}:
        {self.children[0].evaluate()}
        CMP EBX, False
        JE EXIT_{self.id}
        {self.children[1].evaluate()}
        EXIT_{self.id}:
      """


class BinUp(Node):
  """
  @param `value`: operator
  @param `children`: [0] = left operand (expression), [1] = right operand (expression)
  
  """
  def __init__(self, value, children) -> None:
    super().__init__(value=value, children=children)

  def evaluate(self) -> str:
    if self.value == "+":
      return f"""
        ; BinOp +
        MOV EBX, {self.children[0].evaluate()}
        PUSH EBX     ; BinUp guarda resultado no topo da pilha
        MOV EBX, {self.children[1].evaluate()}
        POP EAX      ; BinUp pega o primeiro operando do topo da pilha
        ADD EAX, EBX ; BinUp realiza a operação
        MOV EBX, EAX ; BinUp guarda resultado em EBX
      """
    
    elif self.value == "-":
      return f"""
        ; BinOp -
        MOV EBX, {self.children[0].evaluate()}
        PUSH EBX     ; BinUp guarda resultado no topo da pilha
        MOV EBX, {self.children[1].evaluate()}
        POP EAX      ; BinUp pega o primeiro operando do topo da pilha
        SUB EAX, EBX ; BinUp realiza a operação
        MOV EBX, EAX ; BinUp guarda resultado em EBX
      """
    
    elif self.value == "*":
      return f"""
        ; BinOp *
        MOV EBX, {self.children[0].evaluate()}
        PUSH EBX     ; BinUp guarda resultado no topo da pilha
        MOV EBX, {self.children[1].evaluate()}
        POP EAX       ; BinUp pega o primeiro operando do topo da pilha
        IMUL EAX, EBX ; BinUp realiza a operação
        MOV EBX, EAX  ; BinUp guarda resultado em EBX
      """
    
    elif (self.value == "/"):
      return f"""
        ; BinOp /
        MOV EBX, {self.children[0].evaluate()}
        PUSH EBX     ; BinUp guarda resultado no topo da pilha
        MOV EBX, {self.children[1].evaluate()}
        POP EAX       ; BinUp pega o primeiro operando do topo da pilha
        IDIV EAX, EBX ; BinUp realiza a operação
        MOV EBX, EAX  ; BinUp guarda resultado em EBX
      """

    elif (self.value == "&&"):
      return f"""
        ; BinOp &&
        MOV EBX, {self.children[0].evaluate()}
        PUSH EBX     ; BinUp guarda resultado no topo da pilha
        MOV EBX, {self.children[1].evaluate()}
        POP EAX      ; BinUp pega o primeiro operando do topo da pilha
        AND EAX, EBX ; BinUp realiza a operação
        MOV EBX, EAX ; BinUp guarda resultado em EBX
      """
    
    elif (self.value == "||"):
      return f"""
        ; BinOp ||
        MOV EBX, {self.children[0].evaluate()}
        PUSH EBX     ; BinUp guarda resultado no topo da pilha
        MOV EBX, {self.children[1].evaluate()}
        POP EAX      ; BinUp pega o primeiro operando do topo da pilha
        OR EAX, EBX  ; BinUp realiza a operação
        MOV EBX, EAX ; BinUp guarda resultado em EBX
      """
  
    elif (self.value == ">"):
      return f"""
        ; {self.children[0].value} > {self.children[1].value}
        MOV EBX, {self.children[0].evaluate()}
        PUSH EBX              ; BinUp guarda resultado no topo da pilha
        MOV EBX, {self.children[1].evaluate()}
        POP EAX               ; BinUp pega o primeiro operando do topo da pilha
        CMP EAX, EBX          ; BinUp realiza a operação de comparação
        JG EQUALITY_{self.id} ; Se for maior, pula para a label
        MOV EBX, 0            ; Se não for maior, EBX = 0
        JMP EXIT_{self.id}    ; Pula para o final
        EQUALITY_{self.id}:   ; Label
        MOV EBX, 1            ; Se for maior, EBX = 1
        EXIT_{self.id}:       ; Final do BinOp
      """
    
    elif (self.value == "<"):
      return f"""
        ; {self.children[0].value} < {self.children[1].value}
        MOV EBX, {self.children[0].evaluate()}
        PUSH EBX              ; BinUp guarda resultado no topo da pilha
        MOV EBX, {self.children[1].evaluate()}
        POP EAX               ; BinUp pega o primeiro operando do topo da pilha
        CMP EAX, EBX          ; BinUp realiza a operação de comparação
        JL EQUALITY_{self.id} ; Se for menor, pula para a label
        MOV EBX, 0            ; Se não for menor, EBX = 0
        JMP EXIT_{self.id}    ; Pula para o final
        EQUALITY_{self.id}:   ; Label
        MOV EBX, 1            ; Se for menor, EBX = 1
        EXIT_{self.id}:       ; Final do BinOp
      """
    
    elif (self.value == "=="):
      return f"""
        ; {self.children[0].value} == {self.children[1].value}
        MOV EBX, {self.children[0].evaluate()}
        PUSH EBX              ; BinUp guarda resultado no topo da pilha
        MOV EBX, {self.children[1].evaluate()}
        POP EAX               ; BinUp pega o primeiro operando do topo da pilha
        CMP EAX, EBX          ; BinUp realiza a operação de comparação
        JE EQUALITY_{self.id} ; Se for igual, pula para a label
        MOV EBX, 0            ; Se não for igual, EBX = 0
        JMP EXIT_{self.id}    ; Pula para o final
        EQUALITY_{self.id}:   ; Label
        MOV EBX, 1            ; Se for igual, EBX = 1
        EXIT_{self.id}:       ; Final do BinOp
      """
    
    raise SyntaxError(f"Cannot evaluate a bin operation: {self.children[0].value} {self.value} {self.children[1].value}")
  


class UnOp(Node):
  def __init__(self, value, children) -> None:
    super().__init__(value, children)

  def evaluate(self) -> str:
    if (self.value == "+"):
      return ""
    elif (self.value == "-" or self.value == "!"):
      return """
        NEG EBX
      """
    # elif (self.value == "-"):
    #   return TypeValue("Int", -self.children[0].evaluate().value)
    # elif (self.value == "!"):
    #   return TypeValue("Int", not self.children[0].evaluate().value)
    else:
      raise SyntaxError(f"Invalid unary operation: value = {self.value} :: children = {self.children[0]}")



class IntVal(Node):
  def __init__(self, value: int) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self) -> str:
    return self.value


class StrVal(Node):
  def __init__(self, value: str) -> None:
    super().__init__(value, children=[])
  
  def evaluate(self) -> TypeValue:
    return TypeValue("String", self.value)


class NoOp(Node):
  def __init__(self) -> None:
    super().__init__(value=None, children=None)

  def evaluate(self) -> None:
    pass


class VariableDeclarationNode(Node):
  """
  @param `value`: type of the variable
  @param `children`: [0] = Identifier, [1] = RelExpression
  """
  def __init__(self, value: str) -> None:
    super().__init__(value=value, children=[])
  
  def evaluate(self) -> None:
    if self.value != "Int":
      raise SyntaxError(f"Invalid type of variable declaration: only Int is supported at the moment")
    
    symbol_table.create(self.children[0].value)

    # Se for uma declaração de variável com atribuição
    if len(self.children) > 1:
      return f"""
        ; VarDec with assignment
        PUSH DWORD 0
        MOV EBX, {self.children[1].evaluate()}
        MOV {self.children[0].evaluate()}, EBX
      """
      # item = TypeValue(self.value, self.children[1].evaluate().value)
      # symbol_table.create(self.children[0].value, item)
    
    # Se for uma declaração de variável sem atribuição
    else:
      return f"""
        ; VarDec without assignment
        PUSH DWORD 0
        MOV EBX, 0
        MOV {self.children[0].evaluate()}, EBX
      """
      # if self.value == "Int":
      #   item = TypeValue(self.value, 0)
      # elif self.value == "String":
      #   item = TypeValue(self.value, "")
      # else:
      #   raise SyntaxError(f"Invalid type of variable declaration: {self.value} :: {self.children[0].value}")
      # symbol_table.create(self.children[0].value, item)