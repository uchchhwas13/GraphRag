from langchain_neo4j import Neo4jGraph
from knowledge_graph import graph_documents

# Store Knowledge Graph in Neo4j
graph = Neo4jGraph(
    url="neo4j+s://b7de8794.databases.neo4j.io",
    username="neo4j",
    password="JmaYgn014lSdibCmA8J6vXRMIn5cFVALoRlEmzz_xps",
    database="neo4j"
)

graph.add_graph_documents(graph_documents)
