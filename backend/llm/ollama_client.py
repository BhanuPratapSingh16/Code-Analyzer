import ollama
from config import OLLAMA_MODEL, OLLAMA_HOST
from llm.relation_schema import RelationSchema

class OllamaClient:
    def __init__(self):
        self.model_name = OLLAMA_MODEL
        self.client = ollama.Client(host=OLLAMA_HOST)
    
    def generate(self, system_prompt:str, user_prompt:str):
        messages = []
        
        messages.append({
            "role": "system",
            "content": system_prompt,
        })

        messages.append({
            "role": "user",
            "content": user_prompt,
        })
        response = self.client.chat(
            model=self.model_name,
            messages=messages,
            format=RelationSchema.model_json_schema(),
            think= False,
            options={
                "temperature": 0,
            },
        )

        return response.message.content