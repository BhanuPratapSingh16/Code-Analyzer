from pydantic import BaseModel

class ContainsRelation(BaseModel):
    parent_id: str
    child_id: str
    
class ImportRelation(BaseModel):
    importer_id: str
    importee_id: str
    
class CallRelation(BaseModel):
    callee_id: str
    caller_id: str
    internal_call: bool
    
class InheritRelation(BaseModel):
    sub_id: str
    super_id: str