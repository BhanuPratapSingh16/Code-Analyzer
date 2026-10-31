from retriever.retrieval_schema import RetrievalSchema

class ContextBuilder:
    def __init__(self, max_chars=30000):
        self.max_chars = max_chars
    
    def build_prompt(self, result:RetrievalSchema):
        sections = []
        used_chars = 0
        
        query = result.query
        components = result.components
        relations = result.relations
        modules = result.modules
        
        # Append components
        sections.append("Retrieved Code Components")
        
        for component in components:
            text = f"""
ID: {component.id}
Metadata : {component.metadata}

Document info\n: {component.document}
"""
            if used_chars + len(text) > self.max_chars:
                break
            
            sections.append(text)
            used_chars += len(text)
        
        # Append relations
        component_by_id = {
            component.id: component
            for component in components
        }
        relationship_header = "\nCode Relationships\n"
        if used_chars + len(relationship_header) <= self.max_chars:
            sections.append(relationship_header)
            used_chars += len(relationship_header)

            for edge in relations:
                source = component_by_id.get(edge.source_id)
                target = component_by_id.get(edge.target_id)
                relation = edge.relation
                
                source_name = source.metadata["name"] if source else edge.source_id
                target_name = target.metadata["name"] if target else edge.target_id
                text = f"{source_name} (id: {edge.source_id}) {relation} {target_name} (id: {edge.target_id})\n"
                
                if used_chars + len(text) > self.max_chars:
                    break
                
                sections.append(text)
                used_chars += len(text)

        # Append module components
        module_header = "\nRelated Modules info"
        if used_chars + len(module_header) <= self.max_chars:
            sections.append(module_header)
            for module in modules:
                text = f"""
Module ID : {module.id}
Metadata: {module.metadata}
"""
                if used_chars + len(text) > self.max_chars:
                    break
                            
                sections.append(text)
                used_chars += len(text)
        
        context = "".join(sections)
        
        return (
            f"User question:\n{query}\n\n"
            f"Use the following retrieved code context to answer.\n"
            f"If the context is insufficient, state what is missing "
            f"instead of inventing details.\n\n"
            f"{context}"
        )