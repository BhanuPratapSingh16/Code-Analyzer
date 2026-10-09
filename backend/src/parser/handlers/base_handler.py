from pathlib import Path
from abc import ABC, abstractmethod
from tree_sitter import Tree, Node
from src.components.code_components import Component
from src.relation.mapper import ComponentsMapper

class BaseHandler(ABC):
    @abstractmethod
    def extract_components(self, source_bytes:bytes, file_path:Path, tree:Tree, componentsMapper:ComponentsMapper) -> list[Component]:
        pass