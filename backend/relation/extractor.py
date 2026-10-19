from relation.relation_components import ContainsRelation, ImportRelation
from itertools import chain
from utils.symbol_index import SymbolIndex

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
    
    def extract_imports(self, symbol_index:SymbolIndex):
        imports = []
        module_components = self.components["module"]
        for component in self.components["import"]:
            source = component.file_name
            import_target = component.import_target
            imported_component = component.imported_component
            
            # import statement
            if not imported_component:
                for component in module_components:
                    if component.id == import_target:
                        import_relation = ImportRelation(
                            importer_id= source,
                            importee_id= import_target
                        )
                        imports.append(import_relation)
            # import from statement
            else:
                # If class/function imported
                imported_component_qfn = f"{import_target}:{imported_component}"
                ids = symbol_index.getIndices(imported_component_qfn)
                if ids:
                    for id in ids:
                        import_relation = ImportRelation(
                            importer_id= source,
                            importee_id= id
                        )
                        imports.append(import_relation)
                # If submodule imported
                else:
                    imported_component_qfn = f"{import_target}.{imported_component}"
                    for component in module_components:
                        if component.id == imported_component_qfn:
                            import_relation = ImportRelation(
                                importer_id= source,
                                importee_id= imported_component_qfn
                            )
                            imports.append(import_relation)
                            break
        return imports