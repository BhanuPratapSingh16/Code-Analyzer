from sentence_transformers import SentenceTransformer

class CodeEmbeddor:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        
    def get_text(self, component):
        component_type = type(component).__name__
        file_name = component.file_name
        name = component.name
        code = component.code
        
        return f"""
Component: {component_type}
Name: {name}
File: {file_name}

Code: 
{code}
    """.strip()

    def embed_components(self, components:list):
        texts = [self.get_text(component) for component in components]
        
        embeddings = self.model.encode(texts, batch_size=8, show_progress_bar=True, convert_to_numpy=True)
        return texts, embeddings
    
    def embed_query(self, text):
        return self.model.encode(text, convert_to_numpy=True)