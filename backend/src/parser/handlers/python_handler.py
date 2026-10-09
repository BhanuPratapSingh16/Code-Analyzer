from pathlib import Path
from tree_sitter import Tree, Node
from src.components.code_components import Component, ClassComponent, FunctionComponent
from src.parser.handlers.base_handler import BaseHandler
from src.relation.mapper import ComponentsMapper

class PythonHandler(BaseHandler):
    def extract_components(self, source_bytes:bytes, file_path:Path, tree:Tree, componentsMapper:ComponentsMapper) -> list[Component]:
        components = []
        file_name = str(Path(file_path).with_suffix(""))
        file_id = componentsMapper.get_id_by_name(file_name)
        
        def traverse(node: Node, parent_id: str=file_id, parent_name:str=file_name):
            # Identify node type
            node_type = node.type

            if node_type == "class_definition":
                name_node = node.child_by_field_name("name")
                if name_node:
                    # Extract name and create qualified name
                    class_name = source_bytes[name_node.start_byte:name_node.end_byte].decode("utf-8")
                    class_qualified_name = f"{parent_name}.{class_name}"
                    
                    # Create class node
                    class_component = ClassComponent(
                        name= class_name,
                        qualified_name= class_qualified_name,
                        file_path= file_path,
                        parent_id= parent_id,
                        code= source_bytes[node.start_byte:node.end_byte],
                        start_line= name_node.start_point[0] + 1,
                        end_line= name_node.end_point[0] + 1
                    )
                    components.append(class_component)
                    
                    # Update parent id and parent name
                    parent_id = class_component.id
                    parent_name = class_component.qualified_name
                    componentsMapper.map_name_to_id(parent_name, parent_id)
            
            elif node.type == "function_definition":
                name_node = node.child_by_field_name("name")
                if name_node:
                    # Extract function name and create qualified name
                    func_name = source_bytes[name_node.start_byte:name_node.end_byte]
                    func_qualified_name = f"{parent_name}.{func_name}"
                    
                    # Extract parameters
                    parameters = []
                    params_node = name_node.child_by_field_name("parameters")
                    if params_node:
                        for child in params_node:
                            parameters.append(source_bytes[child.start_byte:child.end].decode("utf-8"))
                            
                    # Extract return type
                    return_node = node.child_by_field_name("return_type")
                    return_type = source_bytes[return_node.start_byte:return_node.end_byte] if return_node else None
                    
                    # Create function node
                    function_component = FunctionComponent(
                        name= func_name,
                        qualified_name= func_qualified_name,
                        file_path= file_path,
                        parent_id= parent_id,
                        code= source_bytes[node.start_byte:node.end_byte].decode("utf-8"),
                        start_line= node.start_point[0]+1,
                        end_line= node.end_point[0]+1,
                        parameters= parameters,
                        return_type= return_type
                    )
                    components.append(function_component)
                    
                    # Update parent id and parent name
                    parent_id = function_component.id
                    parent_name = function_component.qualified_name
                    componentsMapper.map_name_to_id(parent_name, parent_id)

        traverse(tree.root_node)            
        return components