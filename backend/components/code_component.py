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
    
class ModuleComponent(BaseModel):
    path: Path
    name: str
    
class ImportComponent(BaseModel):
    file: Path
    file_name: str
    module_name: str
    alias: str | None = None
    
class CallComponent(BaseModel):
    call_text: str
    callee_name: str | None = None
    caller_name: str
    receiver_name: str | None = None
    method_name: str | None = None
    call_type: str