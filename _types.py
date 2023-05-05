from typing import Any, Union

class TypeValue():
  def __init__(self, _type: str, value: Union[int, str]) -> None:
    if _type not in ["Int", "String"]:
      raise ValueError(f"Invalid type {_type}")
    self._type = _type
    self._value = value

  @property
  def type(self) -> str:
    return self._type
  
  @property
  def value(self) -> Union[int, str]:
    return self._value
  
  @property
  def instance(self):
    return (self._type, self._value)
  
