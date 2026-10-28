import chromadb
import json
from components.code_component import ClassComponent, FunctionComponent
from embeddings.embedder import CodeEmbeddor

class CodeVectorStore:
    def __init__(self, persist_dir:str="chroma_db", collection_name:str="code_component"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
    def add_components(self, components, texts, embeddings):
        ids = []
        metadatas = []
        documents = []
        
        for component, text in zip(components, texts):
            ids.append(str(component.id))
            documents.append(text)
            
            metadata = {
                "name": component.name,
                "type": type(component).__name__,
                "file_path": str(component.file),
                "file": str(component.file_name),
                "parent_id": str(component.parent_id),
                "start_line": int(component.start_line),
                "end_line": int(component.end_line)
            }
            
            if isinstance(component, ClassComponent):
                metadata["bases"] = json.dumps(component.bases)
            
            elif isinstance(component, FunctionComponent):
                metadata["parameters"] = json.dumps(component.parameters)
                metadata["return_type"] = component.return_type
            
            metadatas.append(metadata)
            
        component_embeddings = {}
        for component, embedding in zip(components, embeddings):
            component_embeddings[component.id] = embedding.tolist()

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=[component_embeddings[component_id] for component_id in ids]
        )
    
    def search(self, query:str, embedder:CodeEmbeddor, top_n=4):
        query_embedding = embedder.embed_query(query)
        
        results = self.collection.query(
            query_embeddings= [query_embedding.tolist()],
            n_results= top_n,
            include= ["documents", "metadatas"]
        )
        
        matches = []

        for i, component_id in enumerate(results["ids"][0]):
            matches.append({
                "id": component_id,
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
            })

        return matches
    
    def get_by_id(self, ids:list):
        if not ids:
            return []
        
        res = self.collection.get(ids=ids, include=["documents", "metadatas"])
        components = []
        
        for i, id in enumerate(res["ids"]):
            components.append({
                "id": id,
                "document": res["documents"][i],
                "metadata": res["metadata"][i],
            })
        
        return components