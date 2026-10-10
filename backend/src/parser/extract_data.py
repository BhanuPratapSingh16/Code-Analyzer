from pathlib import Path
from tree_sitter_language_pack import get_parser
from src.parser.handlers.python_handler import PythonHandler
from src.components.code_components import FileComponent
from src.relation.mapper import ComponentsMapper

# Constants
# Map the extension of files to corresponding langauge and tree sitter extractor
LANGUAGE_MAP = {
    ".py": ("python", PythonHandler())
}


def parse_code(ROOT_DIR:str, componentsMapper: ComponentsMapper):
    components = {}
    components["file"] = []
    components["class"] = []
    components["function"] = []
    components["import"] = []
    components["call"] = []
    components["variable"] = []

    # Read all files recursively
    for path in Path(ROOT_DIR).rglob("*"):
        if path.is_file():
            ext = path.suffix
            if ext in LANGUAGE_MAP:
                language, handler = LANGUAGE_MAP.get(ext)

                # Get the parser corresponding to the language
                parser = get_parser(language)

                # Read bytes from file 
                source_bytes = path.read_bytes()

                # Parse the code
                tree = parser.parse(source_bytes)
 
                # Add modular component
                module_component = FileComponent(
                    name= str(path.stem),
                    qualified_name= str(path.with_suffix("")).replace("\\", "."),
                    file_path= path,
                    code= source_bytes.decode("utf-8"),
                    language= language
                )
                components["file"].append(module_component)
                
                # Map module name to its id
                componentsMapper.map_name_to_id(module_component.qualified_name, module_component.id)

                # Extract the components
                extracted_components = handler.extract_components(source_bytes, path, tree, componentsMapper)
                
                # Add code components
                for key, value in extracted_components.items():
                    components[key].extend(value)

    return components