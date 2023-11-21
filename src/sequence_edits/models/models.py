from typing import Literal, TypeVar
from pydantic import BaseModel
import ramda as R

A = TypeVar("A")

Type = Literal["insert", "skip"]
class Edit(BaseModel):
    type: Type
    idx: int
