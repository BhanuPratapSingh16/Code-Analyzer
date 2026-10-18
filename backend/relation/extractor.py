from relation.relation_components import ContainsRelation
from itertools import chain

class RelationExtractor:
    def __init__(self, components):
        self.components = components
    
    def extract_contains(self):
        contains = []
        class_comps = self.components["class"]
        function_comps = self.components["function"]

        for component in chain(class_comps, function_comps):
            id = component.id
            parent_id = component.parent_id
            contains_relation = ContainsRelation(
                parent_id= parent_id,
                child_id= id
            )
            contains.append(contains_relation)
        
        return contains