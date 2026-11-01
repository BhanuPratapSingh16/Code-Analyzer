from google import genai
from llm.relation_schema import RelationSchema
from config import GEMINI_API_KEY, GEMINI_MODEL

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL
    
    def generate(self, prompt:str):
        print("Generating response")
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": 0.2,
            }
        )
        return response.text