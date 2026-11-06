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

    def generate_answer(self, prompt: str) -> str:
        response = self.client.chat(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": 0,
                "num_predict": 512
            },
            keep_alive="10m"
        )

        return response.message.content

    def stream_answer(self, prompt: str):
        stream = self.client.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a code analysis assistant.

                    Answer the user's question directly.

                    Rules:
                    - Give concise answers.
                    - Do not output internal reasoning.
                    - Do not repeat the question.
                    - Use only the provided code context.
                    - Explain relevant dependencies and impacts.
                    - Stop immediately after answering.
                    - Maximum answer length: 100 words.
                    Do not provide step-by-step internal reasoning.
                    Do not repeat information.
                    Provide only:
                    1. Direct impact.
                    2. Affected components.
                    3. Relevant file paths.
                    """
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True,
            think=False,
            options={
                "temperature": 0.1,
                "num_predict": 300,
                "repeat_penalty": 1.1,
            },
            keep_alive="10m"
        )

        for chunk in stream:
            text = chunk.message.content

            if text:
                yield text

