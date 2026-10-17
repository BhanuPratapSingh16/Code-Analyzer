from pathlib import Path
from pydantic import BaseModel

class Component(BaseModel):
    name: str
    id: str
    code: str
    file: Path

class ClassComponent(Component):
    start_line: int
    end_line: int
    
class FunctionComponent(Component):
    parameters: list
    return_type: str | None = None
    start_line: int
    end_line: int