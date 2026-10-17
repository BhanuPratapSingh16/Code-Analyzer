from pathlib import Path
from tree_sitter_language_pack import get_parser
from parser.extractor import extract_components


class Parser:
    def __init__(self, root:Path):
        self.root = root
        self.EXT_MAPPER = {
            ".py": "python"
        }
        self.components = {
            "class": [],
            "function": [],
            "variable": [],
            "import": [],
            "call": []
        }
        
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
            parser = get_parser(language)
            
            # Read the contents of file
            source_code = path.read_bytes()
            
            # Get AST
            tree = parser.parse(source_code)
            
            components = extract_components(tree, source_code, path)
            
            for key, value in components.items():
                self.components[key].extend(value)