from google import genai
from llm.relation_schema import RelationSchema
from config import GEMINI_API_KEY, GEMINI_MODEL

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL
    
    def generate(self, system_prompt:str, user_prompt:str):
        print("Generating response")
        response = self.client.models.generate_content(
            model= self.model,
            contents= f"User question: {user_prompt}",
            config= {
                "system_instruction": system_prompt,
                "response_mime_type": "application/json",
                "response_json_schema": RelationSchema.model_json_schema()
            }
        )
        return response.text