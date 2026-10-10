from pathlib import Path
from tree_sitter import Tree, Node
from src.components.code_components import Component, ClassComponent, FunctionComponent, ImportComponent, CallComponent
from src.parser.handlers.base_handler import BaseHandler
from src.relation.mapper import ComponentsMapper

class PythonHandler(BaseHandler):
    def extract_components(self, source_bytes:bytes, file_path:Path, tree:Tree, components_mapper:ComponentsMapper) -> list[Component]:
        components = {}
        components["file"] = []
        components["class"] = []
        components["function"] = []
        components["import"] = []
        components["call"] = []
        
        file_name = str(Path(file_path).with_suffix(""))
        file_name_with_dots = file_name.replace("\\", ".")
        file_id = components_mapper.get_id_by_name(file_name_with_dots)
        
        def text(node: Node):
            return source_bytes[node.start_byte:node.end_byte].decode("utf-8")
        
        def traverse(node: Node, parent_id: str=file_id, parent_name:str=file_name_with_dots):
            # Identify node type
            node_type = node.type
            if node_type == "class_definition":
                name_node = node.child_by_field_name("name")
                if name_node:
                    # Extract name and create qualified name
                    class_name = text(name_node)
                    class_qualified_name = f"{parent_name}.{class_name}"
                    
                    # Create class node
                    class_component = ClassComponent(
                        name= class_name,
                        qualified_name= class_qualified_name,
                        file_path= file_path,
                        parent_id= parent_id,
                        code= text(node),
                        start_line= node.start_point[0] + 1,
                        end_line= node.end_point[0] + 1
                    )
                    components["class"].append(class_component)
                    
                    # Update parent id and parent name
                    parent_id = class_component.id
                    parent_name = class_component.qualified_name
                    components_mapper.map_name_to_id(parent_name, parent_id)
            
            elif node_type == "function_definition":
                name_node = node.child_by_field_name("name")
                if name_node:
                    # Extract function name and create qualified name
                    func_name = text(name_node)
                    func_qualified_name = f"{parent_name}.{func_name}"
                    
                    # Extract parameters
                    parameters = []
                    params_node = name_node.child_by_field_name("parameters")
                    if params_node:
                        for child in params_node:
                            if child:
                                parameters.append(text(child))
                            
                    # Extract return type
                    return_node = node.child_by_field_name("return_type")
                    return_type = text(return_node) if return_node else None
                    
                    # Create function node
                    function_component = FunctionComponent(
                        name= func_name,
                        qualified_name= func_qualified_name,
                        file_path= file_path,
                        parent_id= parent_id,
                        code= text(node),
                        start_line= node.start_point[0]+1,
                        end_line= node.end_point[0]+1,
                        parameters= parameters,
                        return_type= return_type
                    )
                    components["function"].append(function_component)
                    
                    # Update parent id and parent name
                    parent_id = function_component.id
                    parent_name = function_component.qualified_name
                    components_mapper.map_name_to_id(parent_name, parent_id)
            
            elif node_type == "import_statement":
                for child in node.named_children:
                    if child.type == "aliased_import":
                        name_node = child.child_by_field_name("name")
                        alias_node = child.child_by_field_name("alias")
                        
                        if name_node:
                            name = text(name_node)
                            module_name, dot, imported_name = name.rpartition(".")
                            if not dot:
                                module_name = imported_name
                                imported_name = None
                            
                            import_component = ImportComponent(
                                source= file_path,
                                line = node.start_point[0] + 1,
                                code = text(node),
                                module_name= module_name,
                                imported_name= imported_name,
                                alias= text(alias_node) if alias_node else None
                            )
                            components["import"].append(import_component)
                    
                    elif child.type == "dotted_name":
                        name = text(child)
                        module_name, dot, imported_name = name.rpartition(".")
                        if not dot:
                            module_name = imported_name
                            imported_name = None
                        
                        import_component = ImportComponent(
                            source = file_path,
                            line = node.start_point[0] + 1,
                            code = text(node),
                            module_name= module_name,
                            imported_name= imported_name
                        )
                        components["import"].append(import_component)

            elif node_type == "import_from_statement":
                children = node.named_children
                
                if children:
                    module_node = children[0]
                    module_name = text(module_node)
                    
                    for child in children[1:]:
                        if child.type == "aliased_import":
                            name_node = child.child_by_field_name("name")
                            alias_node = child.child_by_field_name("alias")
                            
                            if name_node:
                                import_component = ImportComponent(
                                    source= file_path,
                                    line = node.start_point[0] + 1,
                                    code = text(node),
                                    module_name= f"{module_name}",
                                    imported_name= text(name_node),
                                    alias= text(alias_node) if alias_node else None
                                )
                                components["import"].append(import_component)
                        
                        elif child.type == "dotted_name":
                            import_component = ImportComponent(
                                source= file_path,
                                line= node.start_point[0] + 1,
                                code= text(node),
                                module_name= f"{module_name}",
                                imported_name= text(child)
                            )
                            components["import"].append(import_component)
            
            elif node_type == "call":
                # Called function node
                function_node = node.child_by_field_name("function")
                
                if function_node:
                    call_component = CallComponent(
                        source= file_path,
                        line= node.start_point[0] + 1,
                        caller_id= parent_id,
                        caller_name= parent_name,
                        call_name= text(function_node),
                        code= text(node)
                    )
                    components["call"].append(call_component)
                
            for child in node.named_children:
                traverse(child, parent_id, parent_name)
        traverse(tree.root_node)            
        return components