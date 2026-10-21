class ParentMapper:
    def __init__(self):
        self.child_to_parent = {}
        self.parent_to_children = {}
    
    def put(self, child:str, parent:str):
        self.child_to_parent[child] = parent
        if not self.parent_to_children.get(parent):
            self.parent_to_children[parent] = []
        self.parent_to_children[parent].append(child)
    
    def getParent(self, child:str):
        return self.child_to_parent.get(child)
    
    def getChildren(self, parent:str):
        return self.parent_to_children.get(parent, [])