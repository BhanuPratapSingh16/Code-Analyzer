from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from google.genai import types

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL
    
    def generate(self, prompt:str):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                thinking_config=types.ThinkingConfig(
                    thinking_level="LOW" 
                )
            ),
        )
        return response.text
    
    def stream_answer(self, prompt:str):
        print("Generating answer")
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                thinking_config=types.ThinkingConfig(
                    thinking_level="LOW" 
                )
            ),
        )
        
        for chunk in response:
            if chunk.text:
                yield chunk.text