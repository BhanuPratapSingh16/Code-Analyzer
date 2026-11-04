from pathlib import Path
from parser.parse_docs import Parser
from relation.extractor import RelationExtractor
from utils.symbol_index import SymbolIndex
from utils.parents_mapper import ParentMapper
from utils.imports_mapper import ImportMapper
from graph.build_graph import GraphBuilder
from graph.query_graph import GraphQuery
from embeddings.embedder import CodeEmbeddor
from vector_store.chroma_store import CodeVectorStore
from retriever.hybrid_retriever import HybridRetriever
from retriever.context_builder import ContextBuilder
from llm.gemini_client import GeminiClient
from llm.ollama_client import OllamaClient
from llm.relation_selector import RelationSelector

class RagPipeline:
    def __init__(self):
        # Parse source code
        self.parser = Parser(Path("data/"))

        self.symbol_index = SymbolIndex()
        self.parent_mapper = ParentMapper()
        self.import_mapper = ImportMapper()

        self.parser.parse(self.symbol_index, self.parent_mapper)

        # Extract relationships
        self.relation_extractor = RelationExtractor(self.parser.components)

        self.relation_extractor.extract(self.symbol_index, self.parent_mapper, self.import_mapper)

        # Build knowledge graph
        self.graph_builder = GraphBuilder()

        self.graph_builder.add_nodes(self.parser.components)

        self.graph_builder.add_edges(self.relation_extractor.relations)

        self.graph_query = GraphQuery(self.graph_builder.graph)

        # Generate embeddings
        self.embedder = CodeEmbeddor()
        self.vector_store = CodeVectorStore()

        components = (self.parser.components["class"] + self.parser.components["function"])

        texts, embeddings = self.embedder.embed_components(components)

        self.vector_store.add_components(components, texts, embeddings)

        # Initialize LLMs
        # Ollama selects graph relationships
        self.ollama_client = OllamaClient()

        self.relation_selector = RelationSelector(self.ollama_client)

        # Gemini generates final answers
        self.gemini_client = GeminiClient()

        # Initialize retriever and context builder
        self.hybrid_retriever = HybridRetriever(self.vector_store, self.graph_query)

        self.context_builder = ContextBuilder()

    def retrieve(self, question: str):
        return self.hybrid_retriever.retrieve(
            question,
            self.embedder,
            self.relation_selector,
            self.graph_builder.graph
        )

    def build_prompt(self, retrieval_result):
        return self.context_builder.build_prompt(retrieval_result)

    def generate_answer(self, prompt: str):
        return self.gemini_client.generate_answer(prompt)

    def ask(self, question: str):
        result = self.retrieve(question)
        prompt = self.build_prompt(result)
        return self.generate_answer(prompt)

    def stream_answer(self, prompt: str):
        return self.gemini_client.stream_answer(prompt)