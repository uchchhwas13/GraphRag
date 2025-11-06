"""Query operations for the knowledge graph."""
from langchain_neo4j import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI


def query_graph(question: str, graph: Neo4jGraph, llm: ChatGoogleGenerativeAI) -> str:
    """Query the knowledge graph and generate an answer.
    
    Args:
        question: The question to answer
        graph: Neo4j graph instance
        llm: LLM instance for entity extraction and answer synthesis
        
    Returns:
        str: The answer to the question
    """
    try:
        # Step 1: Extract entities from the question using LLM
        entity_extraction_prompt = f"""From the following question, extract the main entities (people, places, concepts, dates, etc.) that should be searched in the knowledge graph.

Question: {question}

List the key entities (one per line):"""
        
        entities_response = llm.invoke(entity_extraction_prompt).content
        entities = [e.strip() for e in entities_response.split('\n') 
                   if e.strip() and not e.strip().startswith('#')]
        
        print(f"  Extracted entities: {entities[:3]}...")  # Show first 3
        
        # Step 2: Query the graph for relevant information
        all_results = _search_graph(question, graph)
        
        # Step 3: Format the results for the LLM
        graph_data = _format_graph_results(all_results)
        
        # Step 4: Use LLM to synthesize answer from graph data
        answer = _synthesize_answer(question, graph_data, llm)
        return answer
        
    except Exception as e:
        return f"Error querying graph: {str(e)}"


def _search_graph(question: str, graph: Neo4jGraph) -> list:
    """Search the graph for relevant information.
    
    Args:
        question: The question to search for
        graph: Neo4j graph instance
        
    Returns:
        list: List of query results
    """
    all_results = []
    
    # Search for entities in the question
    search_terms = question.lower().split()
    important_words = [w for w in search_terms if len(w) > 3]  # Filter short words
    
    # Query for each important word
    for term in important_words[:5]:  # Limit to 5 terms
        try:
            # Search for nodes containing the term
            query = f"""
            MATCH (n)-[r]-(m)
            WHERE any(prop in keys(n) WHERE 
                toLower(toString(n[prop])) CONTAINS toLower('{term}'))
               OR any(prop in keys(m) WHERE 
                toLower(toString(m[prop])) CONTAINS toLower('{term}'))
            RETURN n, r, m
            LIMIT 10
            """
            result = graph.query(query)
            if result:
                all_results.extend(result)
        except Exception as e:
            continue
    
    # Also try a general query to get all nodes and relationships
    if not all_results:
        try:
            general_query = "MATCH (n)-[r]-(m) RETURN n, r, m LIMIT 20"
            result = graph.query(general_query)
            if result:
                all_results.extend(result)
        except:
            pass
    
    return all_results


def _format_graph_results(results: list) -> str:
    """Format graph query results as a string.
    
    Args:
        results: List of query results
        
    Returns:
        str: Formatted graph data
    """
    if results:
        return "\n".join([str(r) for r in results[:50]])  # Limit results
    else:
        return "No specific graph data found, but the graph contains information about the topic."


def _synthesize_answer(question: str, graph_data: str, llm) -> str:
    """Synthesize an answer from graph data using LLM.
    
    Args:
        question: The question to answer
        graph_data: Formatted graph data
        llm: LLM instance
        
    Returns:
        str: The synthesized answer
    """
    answer_prompt = f"""You are answering questions based on information from a knowledge graph stored in Neo4j.

Question: {question}

Knowledge Graph Data:
{graph_data}

Provide a clear, concise answer based on the graph data above. If the graph data doesn't contain the answer, say so explicitly.

Answer:"""
    
    answer = llm.invoke(answer_prompt).content
    return answer

