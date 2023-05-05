from _types import TypeValue

class SymbolTable:
  """
  Symbol Table

  This module is responsible for the symbol table, 
  which is a dictionary that stores the variables and their values.

  `{ "x": ("Int", 10), "y": ("String", "Hello World") }`
  """
  def __init__(self) -> None:
    self._table = {}
  
  @property
  def table(self) -> dict:
    return self._table
  
  def create(self, key, value):
    if key in self._table.keys():
      raise SyntaxError(f"Item {key} already exists")
    self._table[key] = value


  def getter(self, item):
    if item in self._table.keys():
      return self._table[item]
    raise SyntaxError(f"Item {item} not found")


  def setter(self, key, value: TypeValue):
    _type, _value = value.instance
    if key not in self._table.keys():
      raise SyntaxError(f"Item {key} not found or not declared")
    if (_type == "Int" and type(_value) != int) or (_type == "String" and type(_value) != str):
      raise SyntaxError(f"Type mismatch: {_type} != {type(_value)}")
    self._table[key] = value


symbol_table = SymbolTable()
