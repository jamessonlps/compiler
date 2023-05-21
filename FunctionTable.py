
class FunctionTable:
  """
  Map the function name to the function object

  `key`: function name\n
  `value`: function object
  """
  def __init__(self) -> None:
    self.table = {}


  def create(self, key: str, value) -> None:
    """
    Create a new function in the table

    `key`: function name\n
    `value`: function object
    """
    if key in self.table.keys():
      raise SyntaxError(f"Function '{key}' already exists")
    self.table[key] = value


  def getter(self, item: str):
    """
    Get a function from the table

    `item`: function name
    """
    if item not in self.table.keys():
      raise SyntaxError(f"Function '{item}' not found")
    return self.table[item]


function_table = FunctionTable()
