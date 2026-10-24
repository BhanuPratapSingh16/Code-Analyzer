from itertools import chain
from pathlib import Path
import networkx as nx

class GraphBuilder:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
    
    def add_nodes(self, components:dict):
        class_components = components["class"]
        function_components = components["function"]
        module_components = components["module"]
        
        for component in chain(class_components, function_components, module_components):
            # Get attributes
            attributes = component.model_dump(exclude={"id"})
            
            # Convert path to string
            for key, value in attributes.items():
                if isinstance(value, Path):
                    attributes[key] = str(value)
            
            # Get kind of component
            attributes["kind"] = type(component).__name__
            
            self.graph.add_node(component.id, **attributes)
    
    def add_relation(self, source_id:str, target_id:str, relation:str):
        if source_id in self.graph and target_id in self.graph:
            self.graph.add_edge(
                source_id,
                target_id,
                relation=relation
            )
    
    def add_edges(self, relations:list):
        print(len(relations))
        for reln in relations:
            self.add_relation(reln.source_id, reln.target_id, reln.relation)
    