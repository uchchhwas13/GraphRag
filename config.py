"""Configuration settings for GraphRAG application."""
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# LLM Configuration
LLM_MODEL = "gemini-flash-latest"
LLM_TEMPERATURE = 0

# Neo4j Configuration
NEO4J_URL = "neo4j://127.0.0.1:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "cefalo2025"

# Document Processing Configuration
CHUNK_SIZE = 200
CHUNK_OVERLAP = 20
INPUT_FILE = "input.txt"

# Graph Schema Configuration
ALLOWED_NODES = [
    "Person",
    "Organization",
    "Location",
    "Event",
    "Date",
    "Concept",
    "Theory"
]

ALLOWED_RELATIONSHIPS = [
    "WORKS_AT",
    "BORN_IN",
    "LIVES_IN",
    "DEVELOPED",
    "WON",
    "INVOLVED_IN",
    "RELATED_TO"
]

