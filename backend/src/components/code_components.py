from pydantic import BaseModel, Field
from uuid import uuid4
from pathlib import Path

class Component(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    qualified_name: str
    file_path: Path
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

class ImportComponent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source: Path
    line: int
    code: str
    module_name: str
    imported_name: str | None = None
    alias: str | None=None
    
class CallComponent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    source: Path
    line: int
    caller_id: str
    caller_name: str
    call_name: str
    code: str