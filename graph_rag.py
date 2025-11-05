from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import Neo4jGraph
from langchain_community.graphs import Neo4jGraph as LangChainNeo4jGraph
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API key from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Load text data
loader = TextLoader("input.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
texts = text_splitter.split_documents(documents)

print(f"Loaded {len(texts)} document chunks")

# Initialize the LLM (using Gemini Flash model - free tier)
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

# Extract knowledge graph
print("Extracting knowledge graph from documents...")
print("Note: This may take a while as Gemini processes each document chunk...")

try:
    # Try with explicit prompt customization
    # LLMGraphTransformer may have issues with Gemini, so let's check what happens
    llm_transformer = LLMGraphTransformer(
        llm=llm,
        allowed_nodes=["Person", "Organization", "Location", "Event", "Date", "Concept", "Theory"],
        allowed_relationships=["WORKS_AT", "BORN_IN", "LIVES_IN", "DEVELOPED", "WON", "INVOLVED_IN", "RELATED_TO"]
    )
    
    print("Converting documents to graph... (this may take a minute)")
    graph_documents = llm_transformer.convert_to_graph_documents(texts)
    print(f"Extracted {len(graph_documents)} graph documents")
except Exception as e:
    print(f"ERROR during graph extraction: {e}")
    print(f"Error details: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    graph_documents = []

# Debug: Check what's in the graph documents
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
        print("\nAttempting manual extraction using Gemini directly...")
        
        # Manual extraction as fallback
        from langchain_community.graphs.graph_document import GraphDocument, Node, Relationship
        
        manually_extracted_docs = []
        for text_doc in texts:
            extraction_prompt = f"""Extract entities and relationships from the following text and return them in a structured format.

Text: {text_doc.page_content[:1000]}

Extract:
1. Entities (people, places, organizations, concepts, dates) with their types
2. Relationships between entities

Format your response as JSON with this structure:
{{
  "entities": [
    {{"id": "unique_id", "name": "Entity Name", "type": "Person|Organization|Location|Event|Date|Concept"}}
  ],
  "relationships": [
    {{"source": "entity_id", "target": "entity_id", "type": "RELATIONSHIP_TYPE"}}
  ]
}}

Only return valid JSON:"""
            
            try:
                response = llm.invoke(extraction_prompt).content
                
                # Try to parse JSON from response
                import json
                import re
                
                # Extract JSON from response (might be wrapped in markdown)
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    
                    # Create nodes and relationships
                    nodes = []
                    node_map = {}
                    for entity in data.get("entities", []):
                        node = Node(id=entity.get("id", entity.get("name")), 
                                   type=entity.get("type", "Entity"),
                                   properties={"name": entity.get("name")})
                        nodes.append(node)
                        node_map[entity.get("id", entity.get("name"))] = node
                    
                    relationships = []
                    for rel in data.get("relationships", []):
                        source_node = node_map.get(rel.get("source"))
                        target_node = node_map.get(rel.get("target"))
                        if source_node and target_node:
                            relationship = Relationship(source=source_node,
                                                      target=target_node,
                                                      type=rel.get("type", "RELATED_TO"))
                            relationships.append(relationship)
                    
                    if nodes or relationships:
                        graph_doc = GraphDocument(nodes=nodes, relationships=relationships, source=text_doc)
                        manually_extracted_docs.append(graph_doc)
                        print(f"  Manually extracted {len(nodes)} nodes and {len(relationships)} relationships from chunk")
            except Exception as e:
                print(f"  Error in manual extraction: {e}")
                continue
        
        if manually_extracted_docs:
            print(f"\n✅ Manually extracted {len(manually_extracted_docs)} graph documents")
            graph_documents = manually_extracted_docs
            # Recalculate totals
            total_nodes = sum(len(doc.nodes) if doc.nodes else 0 for doc in graph_documents)
            total_relationships = sum(len(doc.relationships) if doc.relationships else 0 for doc in graph_documents)
            print(f"Total: {total_nodes} nodes, {total_relationships} relationships")
        else:
            print("\n❌ Manual extraction also failed. Cannot proceed without graph data.")
else:
    print("WARNING: No graph documents extracted!")

# Store Knowledge Graph in Neo4j
print("Storing knowledge graph in Neo4j...")
graph = Neo4jGraph(
    url="neo4j://127.0.0.1:7687",
    username="neo4j",
    password="cefalo2025"
)

# Clear existing data
try:
    graph.query("MATCH (n) DETACH DELETE n")
    print("Cleared existing Neo4j data")
except Exception as e:
    print(f"Note: {e}")

# Add graph documents
if graph_documents:
    print(f"\nAdding {len(graph_documents)} graph documents to Neo4j...")
    try:
        graph.add_graph_documents(graph_documents)
        print("Knowledge graph stored in Neo4j")
    except Exception as e:
        print(f"ERROR adding graph documents: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
else:
    print("ERROR: No graph documents to add!")

# Verify the graph was stored
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

# Create a query chain for answering questions
print("Setting up query chain...")

def query_graph(question):
    """Query the knowledge graph using a more reliable approach"""
    try:
        # Step 1: Extract entities from the question using LLM
        entity_extraction_prompt = f"""From the following question, extract the main entities (people, places, concepts, dates, etc.) that should be searched in the knowledge graph.

Question: {question}

List the key entities (one per line):"""
        
        entities_response = llm.invoke(entity_extraction_prompt).content
        entities = [e.strip() for e in entities_response.split('\n') if e.strip() and not e.strip().startswith('#')]
        
        print(f"  Extracted entities: {entities[:3]}...")  # Show first 3
        
        # Step 2: Query the graph for relevant information
        # Use a simpler approach - search for nodes and their relationships
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
        
        # Step 3: Format the results for the LLM
        if all_results:
            graph_data = "\n".join([str(r) for r in all_results[:50]])  # Limit results
        else:
            graph_data = "No specific graph data found, but the graph contains information about the topic."
        
        # Step 4: Use LLM to synthesize answer from graph data
        answer_prompt = f"""You are answering questions based on information from a knowledge graph stored in Neo4j.

Question: {question}

Knowledge Graph Data:
{graph_data}

Provide a clear, concise answer based on the graph data above. If the graph data doesn't contain the answer, say so explicitly.

Answer:"""
        
        answer = llm.invoke(answer_prompt).content
        return answer
        
    except Exception as e:
        return f"Error querying graph: {str(e)}"

# Query examples
print("\n" + "="*50)
print("Querying the knowledge graph...")
print("="*50 + "\n")

queries = [
    "what is birthdate of Albert Einstein? ",
    "When did he won the nobel prize?",
    "Was he involved in Manhattan project?"
]

for query in queries:
    print(f"Query: {query}")
    answer = query_graph(query)
    print(f"Answer: {answer}\n")
    print("-"*50 + "\n")
