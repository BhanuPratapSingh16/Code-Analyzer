from tree_sitter import Tree, Node
from src.components.code_components import Component
from src.parser.handlers.base_handler import BaseHandler

class PythonHandler(BaseHandler):
    def extract_components(self, source_bytes:bytes, file_path:str, tree:Tree) -> list[Component]:
        components = []

        def traverse(node: Node, parent_id: str=None, parent_name:str = file_path):
            # Identify node type
            node_type = node.type

            pass
            
        return components