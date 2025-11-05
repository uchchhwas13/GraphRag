"""Document loading and text splitting."""
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP, INPUT_FILE


def load_and_split_documents(file_path: str = None) -> list[Document]:
    """Load documents from file and split into chunks.
    
    Args:
        file_path: Path to the input file. Defaults to config.INPUT_FILE
        
    Returns:
        list[Document]: List of document chunks
    """
    if file_path is None:
        file_path = INPUT_FILE
    
    # Load documents
    loader = TextLoader(file_path)
    documents = loader.load()
    
    # Split into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    texts = text_splitter.split_documents(documents)
    
    print(f"Loaded {len(texts)} document chunks")
    return texts

