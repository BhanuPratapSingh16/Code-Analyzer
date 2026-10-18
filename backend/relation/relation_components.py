from pydantic import BaseModel

class ContainsRelation(BaseModel):
    parent_id: str
    child_id: str