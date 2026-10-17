from pathlib import Path
from tree_sitter import Tree, Node, Query, QueryCursor, Language
from components.code_component import ClassComponent, FunctionComponent

class Extractor:
    def __init__(self):
        self.function_queries = {
            "python": "(function_definition name: (identifier) @func_name parameters: (parameters) @params) @func",
            "javascript": "(function_declaration name: (identifier) @func_name) @func",
            "typescript": "(function_declaration name: (identifier) @func_name) @func",
            "java": "(method_declaration name: (identifier) @func_name) @func",
            "cpp": "(function_definition declarator: (function_declarator declarator: (identifier) @func_name) @func)",
            "c": "(function_definition declarator: (function_declarator declarator: (identifier) @func_name) @func)",
        }

        self.class_queries = {
            "python": "(class_definition name: (identifier) @class_name) @class",
            "javascript": "(class_declaration name: (identifier) @class_name) @class",
            "typescript": "(class_declaration name: (identifier) @class_name) @class",
            "java": "(class_declaration name: (identifier) @class_name) @class",
            "cpp": "(class_specifier name: (type_identifier) @class_name) @class",
        }
    
    def __gettext(self, node:Node):
        return node.text.decode("utf-8")
    
    def __getid(self, node:Node, name:str, file_name:str):
        current_node = node
        current_name = name
        
        while True:
            parent = current_node.parent
            
            if not parent:
                break
            
            if parent.type in ("class_definition", "function_definition"):
                name_node = parent.child_by_field_name("name")
            
                parent_name = self.__gettext(name_node)
                current_name = f"{parent_name}:{current_name}"
            
            current_node = parent
            
        start_row = node.start_point[0] + 1
        start_col = node.start_point[1] + 1
        
        return f"{file_name}:{current_name}:{start_row}:{start_col}"
                    
    
    def extract_functions(self, tree:Tree, lang:Language, language:str, path:Path):
        function_comps = []
        
        file_name = str(path.with_suffix("")).replace("\\", ".")
        
        # Execute query and get functions
        query_string = self.function_queries[language]
        query = Query(lang, query_string)
        cursor = QueryCursor(query)
        matches = cursor.matches(tree.root_node)
        
        for _, capture_dict in matches:
            # Extract function name and code
            name_node = capture_dict["func_name"][0]
            func_node = capture_dict["func"][0]
            
            if not name_node or not func_node:
                continue
            
            func_name = self.__gettext(name_node)
            
            # Extract parameters
            params_node = capture_dict["params"][0]
            parameters = []
            
            if params_node:
                for param in params_node.named_children:                
                    parameters.append(param.text.decode("utf-8"))
            
            # Extract return type
            return_node = func_node.child_by_field_name("return_type")
            return_type = return_node.text.decode("utf-8") if return_node else None
            
            # Construct id
            id = self.__getid(func_node, func_name, file_name)
            
            # Create component
            function_component = FunctionComponent(
                name= func_name,
                id= id,
                code= self.__gettext(func_node),
                file= path,
                parameters= parameters,
                return_type= return_type,
                start_line= func_node.start_point[0] + 1,
                end_line= func_node.end_point[0] + 1
            )
            function_comps.append(function_component)
        
        return function_comps
    
    def extract_classes(self, tree:Tree, lang:Language, language:str, path:Path):
        class_comps = []
        
        file_name = str(path.with_suffix("")).replace("\\", ".")
        
        # Execute query and get classes
        query_string = self.class_queries[language]
        query = Query(lang, query_string)
        cursor = QueryCursor(query)
        matches = cursor.matches(tree.root_node)
        
        for _, capture_dict in matches:
            # Extract class name and code
            name_node = capture_dict["class_name"][0]
            class_node = capture_dict["class"][0]
            
            if not name_node or not class_node:
                continue
            
            class_name = self.__gettext(name_node)
            
            # Construct id
            id = self.__getid(class_node, class_name, file_name)
            
            # Create component
            class_component = ClassComponent(
                name= class_name,
                id= id,
                code= self.__gettext(class_node),
                file= path,
                start_line= class_node.start_point[0] + 1,
                end_line= class_node.end_point[0] + 1,
            )
            class_comps.append(class_component)
        
        return class_comps
            