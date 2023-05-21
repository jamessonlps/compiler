from _types import TypeValue

class SymbolTable:
  """
  Symbol Table

  This module is responsible for the symbol table, 
  which is a dictionary that stores the variables and their values.

  `{ "x": ("Int", 10), "y": ("String", "Hello World") }`
  """
  def __init__(self, name) -> None:
    self._table: dict[str, TypeValue] = {}
    self.name = name
  
  @property
  def table(self) -> dict:
    return self._table
  
  def create(self, key: str, value: TypeValue):
    if key in self._table.keys():
      raise SyntaxError(f"Item '{key}' already exists")
    self._table[key] = value


  def getter(self, item: str) -> TypeValue:
    if item in self._table.keys():
      return self._table[item]
    raise SyntaxError(f"Item '{item}' not found on symbol table '{self.name}'")


  def setter(self, key: str, value: TypeValue):
    _type, _value = value.instance
    if key not in self._table.keys():
      raise SyntaxError(f"Item '{key}' not found or not declared on symbol table '{self.name}'")
    type_in_table = self._table[key].type
    if (type_in_table != _type):
      raise SyntaxError(f"Type mismatch: {_type} != {type_in_table}")
    self._table[key] = value


symbol_table = SymbolTable("global")
