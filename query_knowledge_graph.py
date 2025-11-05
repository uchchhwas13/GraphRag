from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core import get_response_synthesizer
from knowledge_graph import llm
from retrieve_knowledge_graph import query_engine


response_synthesizer = get_response_synthesizer(llm=llm,response_mode= ResponseMode.COMPACT,)

from knowledge_graph import llm
def query_and_synthesize(query):
    retrieved_context = query_engine.query(query)
    response = response_synthesizer.synthesize(query, retrieved_context)
    print(f"Query: {query}")
    print(f"Answer: {response}\n")

# Query 1
query_and_synthesize("Where does Sarah work?")

# Query 2
query_and_synthesize("Who works for prismaticAI?")

# Query 3
query_and_synthesize("Does Michael work for the same company as Sarah?")