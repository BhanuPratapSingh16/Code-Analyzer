class SymbolIndex:
    def __init__(self):
        self.index = {}  # Components qualified name -> list[id]
    
    def setIndex(self, name, id):
        if not self.index.get(name):
            self.index[name] = []
        self.index[name].append(id)
        
    def getIndices(self, name):
        return self.index.get(name)