from src.parser.extract_data import parse_code
from src.relation.mapper import ComponentsMapper

ROOT_DIR = "data/"
components_mapper = ComponentsMapper()

components = parse_code(ROOT_DIR, components_mapper)
print(components)
