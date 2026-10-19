class ComponentsMapper:
    def __init__(self):
        self.id_to_component = {}
    
    def map_id_to_component(self, id, component):
        self.id_to_component[id] = component
    
    def get_component_by_id(self, id):
        return self.id_to_component.get(id)