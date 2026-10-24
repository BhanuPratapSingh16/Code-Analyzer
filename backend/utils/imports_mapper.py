class ImportMapper:
    def __init__(self):
        self.map = {}
    
    def put(self, file_name:str, local_name:str, id:str):
        if not self.map.get(file_name):
            self.map[file_name] = {}
        
        if not self.map.get(file_name).get(local_name):
            self.map[file_name][local_name] = []
        self.map[file_name][local_name].append(id)
    
    def get(self, file_name:str, local_name:str):
        return self.map.get(file_name, {}).get(local_name)