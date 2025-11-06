# GraphRAG - Knowledge Graph with Retrieval Augmented Generation

A Python application that extracts knowledge graphs from text documents using Large Language Models (LLMs) and stores them in Neo4j for querying and retrieval.

## Overview

This project implements a Graph-based Retrieval Augmented Generation (GraphRAG) system that:

1. **Extracts** entities and relationships from text documents using Google's Gemini LLM
2. **Stores** the extracted knowledge graph in Neo4j database
3. **Queries** the knowledge graph to answer questions using RAG techniques

## Features

- 📄 Document loading and text chunking
- 🤖 LLM-powered entity and relationship extraction
- 🗄️ Neo4j graph database integration
- 🔍 Knowledge graph querying with natural language
- 🎯 Modular, maintainable codebase

## Prerequisites

- Python 3.8 or higher
- Neo4j database (local or remote)
- Google Gemini API key

## Installation

1. **Clone or navigate to the project directory**

```bash
cd GraphRag
```

2. **Create a virtual environment (recommended)**

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
NEO4J_URL=neo4j://127.0.0.1:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

## Project Structure

```
GraphRag/
├── config.py              # Configuration settings and constants
├── document_loader.py      # Document loading and text splitting
├── llm_setup.py           # LLM initialization
├── graph_extraction.py    # Knowledge graph extraction logic
├── graph_storage.py       # Neo4j storage operations
├── graph_query.py         # Query operations for the knowledge graph
├── graph_rag.py           # Main application entry point
├── input.txt              # Input text file for processing
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Usage

### 1. Prepare Your Input File

Place your text file in the project root as `input.txt`, or modify `INPUT_FILE` in `config.py`.

### 2. Run the Application

```bash
python3 graph_rag.py
```

The application will:
1. Load and split the input document
2. Extract entities and relationships using Gemini LLM
3. Store the knowledge graph in Neo4j
4. Execute sample queries

### 3. Customize Queries

Edit the `queries` list in `graph_rag.py` to ask your own questions:

```python
queries = [
    "When did Einstein make significant contribution in statistical mechanics?",
    "Your custom question here?"
]
```

## Configuration

### LLM Settings

Edit `config.py` to customize:

```python
LLM_MODEL = "gemini-flash-latest"  # Gemini model to use
LLM_TEMPERATURE = 0                # Temperature for LLM responses
```

### Document Processing

```python
CHUNK_SIZE = 200      # Size of text chunks
CHUNK_OVERLAP = 20    # Overlap between chunks
INPUT_FILE = "input.txt"  # Input file path
```

### Graph Schema

Modify allowed node types and relationships in `config.py`:

```python
ALLOWED_NODES = ["Person", "Organization", "Location", ...]
ALLOWED_RELATIONSHIPS = ["WORKS_AT", "BORN_IN", "LIVES_IN", ...]
```

## How It Works

### 1. Document Processing
- Documents are loaded and split into manageable chunks
- Chunks are processed sequentially by the LLM

### 2. Graph Extraction
- The LLM (Gemini) extracts entities and relationships from each chunk
- Extracted data follows a structured format:
  ```json
  [
    {
      "head": "Entity A",
      "head_type": "Person",
      "relation": "WORKS_AT",
      "tail": "Entity B",
      "tail_type": "Organization"
    }
  ]
  ```

### 3. Graph Storage
- Extracted graphs are stored in Neo4j
- Nodes represent entities, edges represent relationships

### 4. Querying
- Questions are processed to extract relevant entities
- Neo4j queries search for matching nodes and relationships
- LLM synthesizes answers from retrieved graph data

## Dependencies

- `langchain-core` - Core LangChain functionality
- `langchain_text_splitters` - Text chunking utilities
- `langchain_community` - Community integrations
- `langchain_neo4j` - Neo4j graph database integration
- `langchain_google_genai` - Google Gemini LLM integration
- `langchain_experimental` - Experimental features (LLMGraphTransformer)
- `python-dotenv` - Environment variable management

## Troubleshooting

### No entities extracted

If you see "0 nodes, 0 relationships":
- Check that your Gemini API key is valid
- Verify the LLM model name is correct
- Ensure your input text contains extractable entities
- Check the prompt format in `graph_extraction.py`

### Neo4j Connection Issues

- Verify Neo4j is running: `neo4j status`
- Check connection URL, username, and password in `.env`
- Ensure Neo4j is accessible at the configured URL

### Import Errors

- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python version
- Check that you're in the virtual environment

## Example Output

```
Loaded 1 document chunks
Extracting knowledge graph from documents...
Converting documents to graph... (this may take a minute)
Extracted 1 graph documents

Debug: Analyzing graph documents...
  Document 1:
    Nodes: 15
    Relationships: 12

Total extracted: 15 nodes, 12 relationships

Storing knowledge graph in Neo4j...
Knowledge graph stored in Neo4j

Verification:
  Nodes in graph: [{'count': 15}]
  Relationships in graph: [{'count': 12}]

Query: When did Einstein make significant contribution in statistical mechanics?
Answer: Einstein made significant contributions to statistical mechanics...
```

## License

This project is for educational purposes.

## Contributing

Feel free to submit issues or pull requests for improvements.

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Uses [Google Gemini](https://ai.google.dev/) for LLM capabilities
- Graph storage powered by [Neo4j](https://neo4j.com/)

