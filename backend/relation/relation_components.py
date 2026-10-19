from pydantic import BaseModel

class ContainsRelation(BaseModel):
    parent_id: str
    child_id: str
    
class ImportRelation(BaseModel):
    importer_id: str
    importee_id: str