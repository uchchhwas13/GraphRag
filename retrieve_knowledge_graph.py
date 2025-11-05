from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import KnowledgeGraphRAGRetriever

from knowledge_db import graph
# Retrieve Knowledge for RAG
graph_rag_retriever = KnowledgeGraphRAGRetriever(storage_context=graph.storage_context, verbose=True)
query_engine = RetrieverQueryEngine.from_args(graph_rag_retriever)