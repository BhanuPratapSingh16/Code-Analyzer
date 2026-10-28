from pydantic import BaseModel, Field
from typing import Literal

class RelationSelection(BaseModel):
    type: Literal["CALLS", "IMPORTS", "CONTAINS", "INHERITS"]
    direction: Literal["IN", "OUT"]
    priority: int = Field(ge=1, le=3)

class RelationSchema(BaseModel):
    intent: str
    relationships: list[RelationSelection]