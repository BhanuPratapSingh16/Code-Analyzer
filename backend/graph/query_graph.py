import networkx as nx

class GraphQuery:
    def __init__(self, graph:nx.MultiDiGraph):
        self.graph = graph
    
    def get_component(self, id:str):
        if id not in self.graph:
            return None
        
        return {"id": id, **self.graph.nodes[id]}
    
    def find_components(self, name:str):
        results = []
        
        for node_id, data in self.graph.nodes(data=True):
            if data.get("name") == name:
                results.append({
                    "id": node_id,
                    **data,
                })
        
        return results
    
    def get_relationships(self, id:str, relation:str, direction:str):
        if id not in self.graph:
            return []
        
        results = []
        
        if direction == "OUT":
            for _, target, _, data in self.graph.out_edges(id, keys=True, data=True):
                edge_relation = data.get("relation", "RELATED_TO")
                
                if edge_relation == relation:
                    results.append(target)
            
        
        if direction == "IN":
            for source, _, _, data in self.graph.in_edges(id, keys=True, data=True):
                edge_relation = data.get("relation", "RELATED_TO")
                
                if edge_relation == relation:
                    results.append(source)
        
        return results
    
    def get_callees(self, id:str):
        return self.get_relationships(id, "CALLS", direction="out")

    def get_callers(self, id:str):
        return self.get_relationships(id, "CALLS", direction="in")

    def get_children(self, id:str):
        return self.get_relationships(id, "CONTAINS", direction="out")

    def get_parent(self, id:str):
        return self.get_relationships(id, "CONTAINS", direction="in")

    def get_importees(self, id:str):
        return self.get_relationships(id, "IMPORTS", direction="out")

    def get_importers(self, id:str):
        return self.get_relationships(id, "IMPORTS", direction="in")
    
    def get_base_classes(self, id:str):
        return self.get_relationships(id, "INHERITS", direction="out")

    def get_derived_classes(self, id:str):
        return self.get_relationships(id, "INHERITS", direction="in")
    