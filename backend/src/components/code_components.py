from pydantic import BaseModel, Field
from uuid import uuid4

class Component(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    qualified_name: str
    file_path: str
    parent_id: str | None = None

class FileComponent(Component):
    code: str | None = None

class ClassComponent(Component):
    code: str
    start_line: int
    end_line: int

class FunctionComponent(Component):
    code: str
    start_line: int
    end_line: int
    parameters: list[str] = Field(default_factory=list)
    return_type: str | None = None
