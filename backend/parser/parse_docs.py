from pathlib import Path
from tree_sitter_language_pack import get_parser, get_language
from parser.extractor import Extractor
from components.code_component import ModuleComponent

class Parser:
    def __init__(self, root:Path):
        self.root = root
        self.EXT_MAPPER = {
            ".py": "python",
            ".java": "java"
        }
        self.components = {
            "class": [],
            "function": [],
            "module": [],
            "import": [],
            "call": []
        }
        
        self.languages = {}
        self.parsers = {}
        
        for _, language in self.EXT_MAPPER.items():
            self.languages[language] = get_language(language)
            self.parsers[language] = get_parser(language)
        
        self.extractor = Extractor()
        
    def parse(self):
        # Parse all the files recursively
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            
            # Check valid files
            extension = path.suffix
            if extension not in self.EXT_MAPPER:
                continue
            
            # Extract language and get corresponding parser
            language = self.EXT_MAPPER[extension]
            lang = self.languages[language]
            parser = self.parsers[language]
            
            # Read the contents of file
            source_code = path.read_bytes()
            
            # Get AST
            tree = parser.parse(source_code)
            
            # Extract various components
            function_comps = self.extractor.extract_functions(tree, lang, language, path)
            self.components["function"].extend(function_comps)
            
            class_comps = self.extractor.extract_classes(tree, lang, language, path)
            self.components["class"].extend(class_comps)
            
            import_comps = self.extractor.extract_imports(tree, lang, language, path)
            self.components["import"].extend(import_comps)
            
            call_comps = self.extractor.extract_calls(tree, lang, language, path)
            self.components["call"].extend(call_comps)
            
            module_comp = ModuleComponent(
                id= str(path.with_suffix("")).replace("\\", "."),
                path= path
            )
            self.components["module"].append(module_comp)