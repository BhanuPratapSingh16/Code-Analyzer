class ComponentsMapper:
    def __init__(self):
        self.component_name_to_id = {}
    
    def map_name_to_id(self, name: str, id: str):
        self.component_name_to_id[name] = id
    
    def get_id_by_name(self, name:str):
        return self.component_name_to_id[name]