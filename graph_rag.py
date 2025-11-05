"""Main GraphRAG application."""
from document_loader import load_and_split_documents
from llm_setup import get_llm
from graph_extraction import extract_graph_from_documents, analyze_graph_documents
from graph_storage import store_knowledge_graph
from graph_query import query_graph


def main():
    """Main execution function."""
    # Load and split documents
    texts = load_and_split_documents()
    
    # Initialize LLM
    llm = get_llm()
    
    # Extract knowledge graph
    graph_documents = extract_graph_from_documents(texts, llm)
    
    # Analyze extracted graph
    total_nodes, total_relationships = analyze_graph_documents(graph_documents)
    
    # Check if extraction was successful
    if total_nodes == 0 and total_relationships == 0:
        print("\n❌ Cannot proceed without graph data. Exiting.")
        return
    
    # Store knowledge graph in Neo4j
    graph = store_knowledge_graph(graph_documents)
    
    # Setup query chain
    print("Setting up query chain...")
    
    # Query examples
    print("\n" + "="*50)
    print("Querying the knowledge graph...")
    print("="*50 + "\n")
    
    queries = [
        "When did Einstein make significant contribution in statistical mechanics?",
        "When did he won the nobel prize?",
        "Was Albert Einstein involved in Manhattan project?"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        answer = query_graph(query, graph, llm)
        print(f"Answer: {answer}\n")
        print("-"*50 + "\n")


if __name__ == "__main__":
    main()
