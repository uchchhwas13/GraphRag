"""Neo4j graph storage operations."""
from langchain_neo4j import Neo4jGraph
from langchain_community.graphs.graph_document import GraphDocument
from config import NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD


def create_neo4j_graph() -> Neo4jGraph:
    """Create and return a Neo4j graph connection.
    
    Returns:
        Neo4jGraph: Configured Neo4j graph instance
    """
    return Neo4jGraph(
        url=NEO4J_URL,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD,
        database="neo4j"
    )


def clear_graph(graph: Neo4jGraph) -> None:
    """Clear all nodes and relationships from the graph.
    
    Args:
        graph: Neo4j graph instance
    """
    try:
        graph.query("MATCH (n) DETACH DELETE n")
        print("Cleared existing Neo4j data")
    except Exception as e:
        print(f"Note: {e}")


def store_graph_documents(graph: Neo4jGraph, graph_documents: list[GraphDocument]) -> None:
    """Store graph documents in Neo4j.
    
    Args:
        graph: Neo4j graph instance
        graph_documents: List of graph documents to store
    """
    if not graph_documents:
        print("ERROR: No graph documents to add!")
        return
    
    print(f"\nAdding {len(graph_documents)} graph documents to Neo4j...")
    try:
        graph.add_graph_documents(graph_documents)
        print("Knowledge graph stored in Neo4j")
    except Exception as e:
        print(f"ERROR adding graph documents: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()


def verify_graph_storage(graph: Neo4jGraph) -> None:
    """Verify that the graph was stored correctly.
    
    Args:
        graph: Neo4j graph instance
    """
    try:
        # Count nodes and relationships
        node_result = graph.query("MATCH (n) RETURN count(n) as count")
        rel_result = graph.query("MATCH ()-[r]->() RETURN count(r) as count")
        print(f"\nVerification:")
        print(f"  Nodes in graph: {node_result}")
        print(f"  Relationships in graph: {rel_result}")
        
        # Show some sample nodes to see what was stored
        sample_nodes = graph.query("MATCH (n) RETURN n LIMIT 3")
        print(f"  Sample nodes: {sample_nodes}\n")
    except Exception as e:
        print(f"Note: Could not verify graph: {e}\n")


def store_knowledge_graph(graph_documents: list[GraphDocument]) -> Neo4jGraph:
    """Complete workflow to store knowledge graph in Neo4j.
    
    Args:
        graph_documents: List of graph documents to store
        
    Returns:
        Neo4jGraph: The Neo4j graph instance
    """
    print("Storing knowledge graph in Neo4j...")
    graph = create_neo4j_graph()
    
    # Clear existing data
    clear_graph(graph)
    
    # Add graph documents
    store_graph_documents(graph, graph_documents)
    
    # Verify storage
    verify_graph_storage(graph)
    
    return graph

