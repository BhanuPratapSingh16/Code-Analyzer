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
    components = []
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
                    name= path.stem,
                    qualified_name= str(path.with_suffix("")),
                    file_path= path,
                    code= source_bytes.decode("utf-8"),
                    language= language
                )
                components.append(module_component)
                
                # Map module name to its id
                componentsMapper.map_name_to_id(path.stem, module_component.id)

                # Extract the components
                extracted_components = handler.extract_components(tree, path, source_bytes, componentsMapper)
                
                # Add code components
                components.extend(extracted_components)


    return components