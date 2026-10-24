from relation.relation_components import Relation
from itertools import chain
from utils.symbol_index import SymbolIndex
from utils.parents_mapper import ParentMapper
from utils.imports_mapper import ImportMapper

class RelationExtractor:
    def __init__(self, components):
        self.components = components
        self.relations = []
    
    def extract_contains(self):
        contains = []
        class_comps = self.components["class"]
        function_comps = self.components["function"]

        for component in chain(class_comps, function_comps):
            id = component.id
            parent_id = component.parent_id
            contains_relation = Relation(
                source_id= parent_id,
                target_id= id,
                relation= "CONTAINS"
            )
            contains.append(contains_relation)
        
        self.relations.extend(contains)
    
    def extract_imports(self, symbol_index:SymbolIndex, import_mapper:ImportMapper):
        imports = []
        module_components = self.components["module"]
        for component in self.components["import"]:
            source = component.file_name
            import_target = component.import_target
            imported_component = component.imported_component
            alias = component.alias
            
            # import statement -> Module imported
            if not imported_component:
                for module_component in module_components:
                    if module_component.id == import_target:
                        local_name = alias if alias else import_target
                        import_relation = Relation(
                            source_id= source,
                            target_id= import_target,
                            relation= "IMPORTS"
                        )
                        imports.append(import_relation)
                        import_mapper.put(source, local_name, import_target)
            # import from statement
            else:
                # If class/function imported
                imported_component_qfn = f"{import_target}:{imported_component}"
                ids = symbol_index.getIndices(imported_component_qfn)
                if ids:
                    for id in ids:
                        local_name = alias if alias else imported_component
                        import_relation = Relation(
                            source_id= source,
                            target_id= id,
                            relation= "IMPORTS"
                        )
                        imports.append(import_relation)
                        import_mapper.put(source, local_name, id)
                # If submodule imported
                else:
                    imported_component_qfn = f"{import_target}.{imported_component}"
                    for module_component in module_components:
                        if module_component.id == imported_component_qfn:
                            local_name = alias if alias else imported_component
                            import_relation = Relation(
                                source_id= source,
                                target_id= imported_component_qfn,
                                relation= "IMPORTS"
                            )
                            imports.append(import_relation)
                            import_mapper.put(source, local_name, imported_component_qfn)
                            break
        self.relations.extend(imports)
    
    def __get_qfn(self, id:str):
        parts = id.split(":")
        if len(parts) > 2:
            return ":".join(parts[:-2])
        elif len(parts) <= 0:
            return None
        return "".join(parts)
    
    def extract_calls(self, symbol_index:SymbolIndex, parent_mapper:ParentMapper, import_mapper:ImportMapper):
        calls = []
        call_comps = self.components["call"]
        
        for x in call_comps:
            caller_id = x.caller_id
            
            call_type = x.call_type
            if call_type == "PLAIN":
                callee_name = x.callee_name
                # Check for function with callee name recursively through caller and its parent
                current = caller_id
                while current:
                    children = parent_mapper.getChildren(current)
                    qfn = self.__get_qfn(current)
                    possible_name = f"{qfn}:{callee_name}"
                    
                    found = False
                    
                    for child in reversed(children):
                        child_qfn = self.__get_qfn(child)
                        if possible_name == child_qfn:
                            call_relation = Relation(
                                source_id= caller_id,
                                target_id= child,
                                relation= "CALLS"
                            )
                            calls.append(call_relation)
                            found = True
                            break
                    if found:
                        break
                    current = parent_mapper.getParent(current)

                # Check if call is made from imported components
                if not found:
                    file_name = x.file_name
                    imports = import_mapper.get(file_name, callee_name)
                    if imports:
                        callee_id = imports[-1]
                        call_relation = Relation(
                            source_id= caller_id,
                            target_id= callee_id,
                            relation= "CALLS"
                        )
                        calls.append(call_relation)
            
            elif call_type == "ATTRIBUTE":
                receiver_name = x.receiver_name
                method_name = x.method_name
                file_name = x.file_name

                # Check if call made from another module
                found = False
                imports = import_mapper.get(file_name, receiver_name)

                if imports:
                    module_id = imports[-1]
                    children = parent_mapper.getChildren(module_id)
                    for child in reversed(children):
                        if self.__get_qfn(child) == f"{module_id}:{method_name}":
                            call_relation = Relation(
                                source_id= caller_id,
                                target_id= child,
                                relation= "CALLS"
                            )
                            calls.append(call_relation)
                            found = True
                            break
                    
                if found:
                    continue
                
                # Resolve object based calls
                # Includes -> self, instance based calls
                if receiver_name == "self":
                    # Get parent class
                    current = caller_id
                    flag = False
                    while current and not flag:
                        for comp in self.components["class"]:
                            if comp.id == current:
                                func_qfn = f"{self.__get_qfn(comp.id)}:{method_name}"
                                callee_id = symbol_index.getIndices(func_qfn)
                                if callee_id:
                                    callee_id = callee_id[-1]
                                    call_relation = Relation(
                                        source_id= caller_id,
                                        target_id= callee_id,
                                        relation= "CALLS"
                                    )
                                    calls.append(call_relation)
                                    flag = True
                                    break
                        current = parent_mapper.getParent(current)
        
        self.relations.extend(calls)

    
    def extract_inherits(self, symbol_index:SymbolIndex):
        inherits = []
        class_components = self.components["class"]
        
        for comp in class_components:
            super_id = comp.id
            bases = comp.bases
            file_name = comp.file_name
            for base in bases:
                qfn = f"{file_name}:{base}"
                ids = symbol_index.getIndices(qfn)
                if ids:
                    id = ids[-1]
                    inherit_reln = Relation(
                        source_id= super_id,
                        target_id= id,
                        relation= "INHERITS"
                    )
                    inherits.append(inherit_reln)
        
        self.relations.extend(inherits)

    def extract(self, symbol_index:SymbolIndex, parent_mapper:ParentMapper, import_mapper:ImportMapper):
        self.extract_contains()
        self.extract_calls(symbol_index, parent_mapper, import_mapper)
        self.extract_imports(symbol_index, import_mapper)
        self.extract_inherits(symbol_index)