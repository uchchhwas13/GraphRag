from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from graph_rag import texts
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API key from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set it in environment so LangChain / Google client can detect it
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize the LLM (using Gemini Flash model - free tier)
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

# Extract knowledge graph
llm_transformer = LLMGraphTransformer(llm=llm)
graph_documents = llm_transformer.convert_to_graph_documents(texts)
