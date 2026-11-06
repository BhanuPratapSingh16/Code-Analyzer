from pydantic import BaseModel

class Relation(BaseModel):
    source_id: str
    target_id: str
    relation: str