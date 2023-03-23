class SymbolTable:
  def __init__(self) -> None:
    self._table = {}
  
  @property
  def table(self) -> dict:
    return self._table
  
  def getter(self, item):
    if item in self._table.keys():
      return self._table[item]
    raise SyntaxError(f"Item {item} not found")
  
  def setter(self, key, value):
    self._table[key] = value


symbol_table = SymbolTable()
