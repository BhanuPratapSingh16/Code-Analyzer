from parser.parse_docs import Parser
from pathlib import Path
from relation.extractor import RelationExtractor
from utils.symbol_index import SymbolIndex
from utils.parents_mapper import ParentMapper
from utils.imports_mapper import ImportMapper
from utils.components_mapper import ComponentsMapper
from graph.build_graph import GraphBuilder
from graph.query_graph import GraphQuery
from embeddings.embedder import CodeEmbeddor
from vector_store.chroma_store import CodeVectorStore
from retriever.hybrid_retriever import HybridRetriever
from llm.gemini_client import GeminiClient
from llm.ollama_client import OllamaClient
from llm.relation_selector import RelationSelector
from retriever.context_builder import ContextBuilder

parser = Parser(Path("data/"))

symbol_index = SymbolIndex()
parent_mapper = ParentMapper()
import_mapper = ImportMapper()
components_mapper = ComponentsMapper()
parser.parse(symbol_index, parent_mapper)

# for x in parser.components["import"]:
    # print(x)
reln_extractor = RelationExtractor(parser.components)

reln_extractor.extract(symbol_index, parent_mapper, import_mapper)

# for comp in reln_extractor.relations:
#     if comp.relation == "CALLS":
#         print(comp)

graph = GraphBuilder()
graph.add_nodes(parser.components)
graph.add_edges(reln_extractor.relations)
    
from pyvis.network import Network

def visualize_graph(graph):
    net = Network(
        height="750px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="black"
    )

    # Add nodes
    for node_id, data in graph.nodes(data=True):
        kind = data.get("kind", "Component")
        label = data.get("name", str(node_id))

        net.add_node(
            str(node_id),
            label=label,
            title=f"ID: {node_id}\nType: {kind}",
            group=kind
        )

    # Add edges
    for source, target, data in graph.edges(data=True):
        relation = data.get("relation", "RELATED_TO")

        net.add_edge(
            str(source),
            str(target),
            title=relation,
            label=relation,
            arrows="to"
        )

    net.show("code_graph.html", notebook=False)

# visualize_graph(graph.graph)

graph_query = GraphQuery(graph.graph)

# res = query.find_components("afdf")
# print(res)

# res = query.get_component(res[0]["id"])
# print(res)

# res = query.get_callers(res[0]['id'])
# print(res)

# res = graph_query.find_components("func")
# print(res)
# print(graph_query.get_parent(res[0]["id"]))

embedder = CodeEmbeddor()
vector_store = CodeVectorStore()

cls_func_comps = parser.components["class"] + parser.components["function"]
texts, embeddings = embedder.embed_components(cls_func_comps)

vector_store.add_components(cls_func_comps, texts, embeddings)

query = "What breaks if class AN is deleted?"

hybrid_retriever = HybridRetriever(vector_store, graph_query)


gemini_client = OllamaClient()
relation_selector = RelationSelector(gemini_client)

res = hybrid_retriever.retrieve(query, embedder, relation_selector, graph.graph)
context_builder = ContextBuilder()
prompt = context_builder.build_prompt(res)

gemini_client = GeminiClient()
resp = gemini_client.generate(prompt)

print(resp)