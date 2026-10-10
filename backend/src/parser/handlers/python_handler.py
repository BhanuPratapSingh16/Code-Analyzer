from pathlib import Path
from tree_sitter import Tree, Node
from src.components.code_components import Component, ClassComponent, FunctionComponent, ImportComponent, CallComponent, VariableComponent
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
        components["variable"] = []
        
        file_name = str(Path(file_path).with_suffix(""))
        file_name_with_dots = file_name.replace("\\", ".")
        file_id = components_mapper.get_id_by_name(file_name_with_dots)
        
        def text(node: Node):
            return source_bytes[node.start_byte:node.end_byte].decode("utf-8")
        
        def add_import(node:Node, module_name:str, imported_name:str, alias_node:Node = None):
            import_component = ImportComponent(
                source= file_path,
                line = node.start_point[0] + 1,
                code = text(node),
                module_name= module_name,
                imported_name= imported_name,
                alias= text(alias_node) if alias_node else None
            )
            components["import"].append(import_component)
        
        
        # Function to identify global variables components
        def extract_variables(root=tree.root_node, parent_id:str=file_id, parent_name:str=file_name_with_dots):
            variables = []
            
            for node in root.named_children:
                if node.type not in ("assignment", "annotated_assignment"):
                    continue
                
                # Variable node
                target = node.child_by_field_name("left")
                
                if target is None or target.type != "identifier":
                    continue

                name = text(target)
                type_node = node.child_by_field_name("type")
                
                variable_component = VariableComponent(
                    name=name,
                    qualified_name=f"{parent_name}.{name}",
                    file_path=str(file_path),
                    parent_id= parent_id,
                    code=text(node),
                    line=node.start_point[0] + 1,
                    type_annotation=text(type_node) if type_node else None,
                )
                components["variable"].append(variable_component)
        
        # Recursive functions to identify various components
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
                            
                            add_import(node, module_name, imported_name, alias_node)
                    
                    elif child.type == "dotted_name":
                        name = text(child)
                        module_name, dot, imported_name = name.rpartition(".")
                        if not dot:
                            module_name = imported_name
                            imported_name = None

                        add_import(node, module_name, imported_name)                        

            elif node_type == "import_from_statement":
                children = node.named_children
                
                if children:
                    # First child is module
                    module_node = children[0]
                    module_name = text(module_node)
                    
                    # Others are submodules 
                    for child in children[1:]:
                        if child.type == "aliased_import":
                            name_node = child.child_by_field_name("name")
                            alias_node = child.child_by_field_name("alias")
                            
                            if name_node:
                                add_import(node, module_name, text(name_node), alias_node)
                        
                        elif child.type == "dotted_name":
                            add_import(node, module_name, text(child))
            
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
        extract_variables()
        return components