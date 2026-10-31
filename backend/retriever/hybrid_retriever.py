from itertools import chain
from vector_store.chroma_store import CodeVectorStore
from embeddings.embedder import CodeEmbeddor
from graph.query_graph import GraphQuery
from llm.relation_selector import RelationSelector
from retriever.retrieval_schema import RetrievalSchema, RetrievedRelationship, RetrievedComponent, RetrievedModule
from networkx import MultiDiGraph

class HybridRetriever:
    def __init__(self, vector_store:CodeVectorStore, graph_query:GraphQuery):
        self.vector_store = vector_store
        self.graph_query = graph_query
        
    def retrieve(self, query:str, embedder:CodeEmbeddor, relation_selector:RelationSelector, graph: MultiDiGraph):
        # Select relevant nodes from vector store based on user query
        search_results = self.vector_store.search(query, embedder, top_n=3)

        # Get relevant relationships
        plan = relation_selector.select(query)

        relations_selection = sorted(
            plan.relationships,
            key=lambda relation: relation.priority,
        )[:3]

        # Get related nodes from knowledge graph
        retrieved_relations = []
        related_components_ids = []
        
        for res in search_results:
            id = res["id"]
            
            for relation_selection in relations_selection:
                relation = relation_selection.type
                direction = relation_selection.direction

                related_nodes_id = self.graph_query.get_relationships(id, relation, direction)
                related_components_ids.extend(related_nodes_id)
                
                # Get retrieved relations for constructing retrieval schema
                for node_id in related_nodes_id:
                    source_id = id if direction == "OUT" else node_id
                    target_id = node_id if direction == "OUT" else id
                    
                    retrieved_relations.append(
                        RetrievedRelationship(
                            source_id= source_id,
                            target_id= target_id,
                            relation= relation
                        )
                    )

        # Fetch related components from vector store
        vector_components = self.vector_store.get_by_id(related_components_ids)
        vector_components_ids = [x["id"] for x in vector_components]
        
        retrieved_components = []
        for x in chain(search_results, vector_components):
            retrieved_components.append(
                RetrievedComponent(
                    id= x["id"],
                    document= x["document"],
                    metadata= x["metadata"],
                )
            )
        
        # Get module metadata
        module_ids = list(set(related_components_ids) - set(vector_components_ids))
        retrieved_modules = []
        
        for module_id in module_ids:
            if graph.has_node(module_id):
                module_data = graph.nodes[module_id]
                retrieved_modules.append(
                    RetrievedModule(
                        id= module_id,
                        metadata= module_data
                    )
                )
        
        # Construct retrieval schema
        retrieval_schema = RetrievalSchema(
            query= query,
            components= retrieved_components,
            relations= retrieved_relations,
            modules= retrieved_modules
        )
        return retrieval_schema