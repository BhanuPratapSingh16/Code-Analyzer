from abc import ABC, abstractmethod
from tree_sitter import Tree, Node
from src.components.code_components import Component

class BaseHandler(ABC):
    @abstractmethod
    def extract_components(self, source_bytes:bytes, file_path:str, tree:Tree) -> list[Component]:
        pass