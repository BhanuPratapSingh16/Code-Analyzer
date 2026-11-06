from llm.relation_schema import RelationSchema
from llm.ollama_client import OllamaClient

class RelationSelector:
    SYSTEM_PROMPT = """
You are a relationship selector for a code graph retrieval system.

These are the available relations:

RELATIONS = ['CALLS', 'IMPORTS', 'CONTAINS', 'INHERITS']
DIRECTIONS = ['IN', 'OUT']

CALLS:
 -in: function that is called by a component
 -out: function that is calling another component

IMPORTS:
 -in: component that is imported by another module
 -out: module that is importing another component
 
CONTAINS:
 -in: component contained by another component
 -out: component containing another component

INHERITS:
 -in: class inherited by another class
 -out: class inheriting another class


Instructions:
1. Select only relationships relevant to the user's question.
2. Assign each selected relationship a unique integer priority.
3. Priority 1 is the most important, priority 2 is the next most
   important, and so on.
4. Never assign the same priority to two relationships.
5. Priorities must be consecutive integers starting from 1.
6. Return only output matching the provided JSON schema.
"""
    
    def __init__(self, client:OllamaClient):
        self.client = client
    
    def select(self, query:str):
        response = self.client.generate(self.SYSTEM_PROMPT, query)
        return RelationSchema.model_validate_json(response)