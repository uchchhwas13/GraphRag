"""LLM initialization and setup."""
from langchain_google_genai import ChatGoogleGenerativeAI
from config import LLM_MODEL, LLM_TEMPERATURE


def get_llm() -> ChatGoogleGenerativeAI:
    """Initialize and return the LLM instance.
    
    Returns:
        ChatGoogleGenerativeAI: Configured Gemini LLM instance
    """
    return ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)

