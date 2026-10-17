from pathlib import Path
from tree_sitter import Tree, Node
from components.code_component import ClassComponent, FunctionComponent

def extract_components(tree: Tree, source_code:bytes, path:Path):
    file_name = str(path.with_suffix("")).replace("\\", ".")
    components = {
        "class": [],
        "function": [],
        "variable": [],
        "import": [],
        "call": []
    }
    
    def traverse(node:Node, current_name:str):
        node_type = node.type
        
        def get_text(node:Node):
            return source_code[node.start_byte:node.end_byte].decode("utf-8")
        
        if node_type == "class_definition":
            name_node = node.child_by_field_name("name")
            if name_node:
                class_name = get_text(name_node)
                start_row = node.start_point[0] + 1
                start_col = node.start_point[1] + 1
                end_row = node.end_point[0] + 1
                class_id = f"{current_name}:{class_name}:{start_row}:{start_col}"
                
                class_component = ClassComponent(
                    name= class_name,
                    id= class_id,
                    code= get_text(node),
                    file= path,
                    start_line= start_row,
                    end_line= end_row
                )
                components["class"].append(class_component)
                current_name = f"{current_name:class_name}"
                
        elif node_type == "function_defintion":
            # Extract function name
            name_node = node.child_by_field_name("name")
            function_name = get_text(name_node)
            
            # Extract parameters
            params_node = node.child_by_field_name("parameters")
            parameters= []
            
            if params_node:
                for param in params_node.named_children:
                    parameters.append(get_text(param))
            
            # Extract return type
            return_node = node.child_by_field_name("return_type")
            return_type = get_text(return_node) if return_node else None
            
            start_row = node.start_point[0] + 1
            start_col = node.start_point[1] + 1
            end_row = node.end_point[0] + 1
            function_id = f"{current_name}:{function_name}:{start_row}:{start_col}"
            
            function_component = FunctionComponent(
                name= function_name,
                id= function_id,
                code= get_text(node),
                file= path,
                parameters= parameters,
                return_type= return_type,
                start_line= start_row,
                end_line= end_row
            )
            
            components["function"].append(function_component)
    
    traverse(tree.root_node, file_name)
    return components