"""Knowledge graph extraction from documents using LLM."""
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.graphs.graph_document import GraphDocument
from config import ALLOWED_NODES, ALLOWED_RELATIONSHIPS


def create_extraction_prompt() -> ChatPromptTemplate:
    """Create the prompt template for graph extraction.
    
    Returns:
        ChatPromptTemplate: Configured prompt template
    """
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a top-tier algorithm designed for extracting information in structured formats to build a knowledge graph. "
            "Your task is to identify entities and relations from the given text. "
            "You must generate the output in a JSON format containing a list with JSON objects. "
            "Each object should have the keys: \"head\", \"head_type\", \"relation\", \"tail\", and \"tail_type\". "
            "The \"head\" key must contain the text of the extracted entity. "
            "The \"head_type\" key must contain the type of the extracted head entity "
            "(one of: Person, Organization, Location, Event, Date, Concept, Theory). "
            "The \"relation\" key must contain the type of relation between the \"head\" and the \"tail\" "
            "(one of: WORKS_AT, BORN_IN, LIVES_IN, DEVELOPED, WON, INVOLVED_IN, RELATED_TO). "
            "The \"tail\" key must represent the text of an extracted entity which is the tail of the relation, "
            "and the \"tail_type\" key must contain the type of the tail entity. "
            "Attempt to extract as many entities and relations as you can. "
            "Return ONLY valid JSON"
        ),
        ("human", "Extract entities and relationships from the following text:\n\n{input}")
    ])


def extract_graph_from_documents(
    documents: list[Document],
    llm,
    prompt: ChatPromptTemplate = None
) -> list[GraphDocument]:
    """Extract knowledge graph from documents using LLM.
    
    Args:
        documents: List of document chunks to process
        llm: LLM instance to use for extraction
        prompt: Optional custom prompt template
        
    Returns:
        list[GraphDocument]: List of extracted graph documents
    """
    if prompt is None:
        prompt = create_extraction_prompt()
    
    print("Extracting knowledge graph from documents...")
    print("Note: This may take a while as Gemini processes each document chunk...")
    
    try:
        llm_transformer = LLMGraphTransformer(
            llm=llm,
            allowed_nodes=ALLOWED_NODES,
            allowed_relationships=ALLOWED_RELATIONSHIPS,
            prompt=prompt
        )
        
        print("Converting documents to graph... (this may take a minute)")
        graph_documents = llm_transformer.convert_to_graph_documents(documents)
        print(f"Extracted {len(graph_documents)} graph documents")
        return graph_documents
        
    except Exception as e:
        print(f"ERROR during graph extraction: {e}")
        print(f"Error details: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return []


def analyze_graph_documents(graph_documents: list[GraphDocument]) -> tuple[int, int]:
    """Analyze extracted graph documents and return statistics.
    
    Args:
        graph_documents: List of graph documents to analyze
        
    Returns:
        tuple[int, int]: Total number of nodes and relationships
    """
    total_nodes = 0
    total_relationships = 0
    
    if graph_documents:
        print(f"\nDebug: Analyzing graph documents...")
        for i, doc in enumerate(graph_documents):
            nodes_count = len(doc.nodes) if doc.nodes else 0
            rels_count = len(doc.relationships) if doc.relationships else 0
            total_nodes += nodes_count
            total_relationships += rels_count
            
            if i == 0:  # Detailed info for first document
                print(f"  Document {i+1}:")
                print(f"    Nodes: {nodes_count}")
                print(f"    Relationships: {rels_count}")
                if nodes_count > 0:
                    print(f"    Sample nodes: {[str(n)[:50] for n in doc.nodes[:2]]}")
                if rels_count > 0:
                    print(f"    Sample relationships: {[str(r)[:50] for r in doc.relationships[:2]]}")
        
        print(f"\nTotal extracted: {total_nodes} nodes, {total_relationships} relationships")
        
        if total_nodes == 0 and total_relationships == 0:
            print("\n⚠️  WARNING: No entities or relationships extracted by LLMGraphTransformer!")
            print("This likely means LLMGraphTransformer is not compatible with Gemini's response format.")
            return total_nodes, total_relationships
    else:
        print("WARNING: No graph documents extracted!")
    
    return total_nodes, total_relationships

