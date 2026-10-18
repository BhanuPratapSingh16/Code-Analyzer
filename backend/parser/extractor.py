from pathlib import Path
from tree_sitter import Tree, Node, Query, QueryCursor, Language
from components.code_component import ClassComponent, FunctionComponent, ImportComponent, CallComponent

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
        
        self.import_queries = {
            "python": ["(import_statement) @import", "(import_from_statement) @import"],
            "javascript": ["(import_statement) @import"],
            "typescript": ["(import_statement) @import"],
            "java": ["(import_declaration) @import"],
            "c": ["(preproc_include) @import"],
            "cpp": ["(preproc_include) @import"]
        }

        self.call_queries = {
            "python": ["(call function: (identifier) @callee) @call", "(call function: (attribute object: (_) @receiver attribute: (identifier) @method)) @call"]
        }
        
    def __gettext(self, node:Node):
        return node.text.decode("utf-8")
    
    def __is_function_node(self, node:Node, language:str):
        function_types = {
            "python": ["function_definition"],
            "javascript": ["function_declaration", "arrow_function"],
            "typescript": ["function_declaration", "arrow_function"],
            "java": ["method_declaration"],
            "cpp": ["function_definition"],
            "c": ["function_definition"],
        }
        return node.type in function_types.get(language, [])
        
    def __is_class_node(self, node:Node, language:str):
        class_types = {
            "python": ["class_definition"],
            "javascript": ["class_declaration"],
            "typescript": ["class_declaration"],
            "java": ["class_declaration"],
            "cpp": ["class_specifier"],
        }
        return node.type in class_types.get(language, [])        
    
    def __get_parent_name(self, node:Node, file_name:str, language:str):
        current_node = node
        current_name = None
        while True:
            parent = current_node.parent
            if not parent:
                break
            
            if self.__is_function_node(parent, language) or self.__is_class_node(parent, language):
                name_node = parent.child_by_field_name("name")
                parent_name = self.__gettext(name_node)
                current_name = f"{parent_name}:{current_name}" if current_name else parent_name
            
            current_node = parent
        
        return f"{file_name}:{current_name}" if current_name else file_name
    
    def __getid(self, node:Node, name:str, file_name:str, language:str):
        parent_name = self.__get_parent_name(node, file_name, language)
            
        start_row = node.start_point[0] + 1
        start_col = node.start_point[1] + 1
        
        return f"{parent_name}:{name}:{start_row}:{start_col}"
                    
    
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
            id = self.__getid(func_node, func_name, file_name, language)
            
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
            id = self.__getid(class_node, class_name, file_name, language)
            
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
    
    def extract_imports(self, tree:Tree, lang:Language, language:str, path:Path):
        import_comps = []
        
        file_name = str(path.with_suffix("")).replace("\\", ".")
        
        # Execute against all queries of a languages
        query_strings = self.import_queries[language]
        
        for query_string in query_strings:
            query = Query(lang, query_string)
            cursor = QueryCursor(query)
            matches = cursor.matches(tree.root_node)
            
            for _, capture_dict in matches:
                import_node = capture_dict["import"][0]
                
                if import_node.type == "import_statement":
                    module_node = import_node.child_by_field_name("name")
                    if module_node.type == "dotted_name":
                        module_name = self.__gettext(module_node)
                        alias = None
                    
                    elif module_node.type == "aliased_import":
                        module_name = self.__gettext(module_node.child_by_field_name("name"))
                        alias = self.__gettext(module_node.child_by_field_name("alias"))
                        
                    import_component = ImportComponent(
                        file= path,
                        file_name= file_name,
                        module_name= module_name,
                        alias= alias
                    )
                    import_comps.append(import_component)
                
                elif import_node.type == "import_from_statement":
                    module_node = import_node.child_by_field_name("module_name")
                    module_name = self.__gettext(module_node)
                    
                    imported_node = import_node.child_by_field_name("name")
                    if imported_node.type == "dotted_name":
                        imported_name = self.__gettext(imported_node)
                        alias = None
                    
                    elif imported_node.type == "aliased_import":
                        imported_name = self.__gettext(imported_node.child_by_field_name("name"))
                        alias = self.__gettext(imported_node.child_by_field_name("alias"))
                    
                    import_component = ImportComponent(
                        file= path,
                        file_name= file_name,
                        module_name= f"{module_name}.{imported_name}",
                        alias= alias
                    )
                    import_comps.append(import_component)
        
        return import_comps
    
    def extract_calls(self, tree:Tree, lang:Language, language:str, path:Path):
        call_comps = []
        
        file_name = str(path.with_suffix("")).replace("\\", ".")
        
        query_strings = self.call_queries.get(language)
        
        for query_string in query_strings:
            query = Query(lang, query_string)
            cursor = QueryCursor(query)
            matches = cursor.matches(tree.root_node)
            
            for _, capture_dict in matches:
                call_node = capture_dict["call"][0]
                # Plain calls
                callee_node = capture_dict.get("callee")
                if callee_node:
                    callee_node = callee_node[0]
                    call_type = "PLAIN"
                
                # Attribute calls
                receiver_node = capture_dict.get("receiver")
                method_node = capture_dict.get("method")
                
                if receiver_node and method_node:
                    receiver_node = receiver_node[0]
                    method_node = method_node[0]
                    call_type = "ATTRIBUTE"
                
                # Get caller name
                caller_name = self.__get_parent_name(call_node, file_name, language)
                
                call_component = CallComponent(
                    call_text= self.__gettext(call_node),
                    callee_name= self.__gettext(callee_node) if callee_node else None,
                    caller_name= caller_name,
                    receiver_name= self.__gettext(receiver_node) if receiver_node else None,
                    method_name= self.__gettext(method_node) if method_node else None,
                    call_type= call_type
                )
                call_comps.append(call_component)
        
        return call_comps