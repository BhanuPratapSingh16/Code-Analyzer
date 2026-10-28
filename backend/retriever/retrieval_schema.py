from pydantic import BaseModel

class RetrievedComponent(BaseModel):
    id: str
    code: str
    metadata: dict

class RetrievedRelationship(BaseModel):
    source_id: str
    target_id: str
    relation: str

class RetrievalSchema(BaseModel):
    query:str
    components: list[RetrievedComponent]
    relations: list[RetrievedRelationship]