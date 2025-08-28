# RAG End-to-End Application

A comprehensive Retrieval-Augmented Generation (RAG) application with FastAPI backend and Streamlit frontend.

## Project Structure

```
end_to_end/
├── api/                    # FastAPI backend
│   ├── __init__.py
│   ├── main.py            # Main API endpoints
│   ├── pydantic_models.py # Data models
│   └── app.log           # API logs
├── frontend/              # Streamlit frontend
│   ├── __init__.py
│   ├── streamlit_app.py   # Main Streamlit app
│   ├── chat_interface.py  # Chat interface
│   ├── sidebar.py         # Sidebar components
│   └── api_utils.py       # Frontend API utilities
├── utilities/              # Shared utilities
│   ├── __init__.py
│   ├── constants.py       # All configuration constants
│   ├── chroma_utils.py    # ChromaDB and vector store operations
│   ├── langchain_utils.py # LangChain utilities
│   └── db.py              # Database operations
├── scripts/                # Standalone scripts
│   ├── __init__.py
│   ├── evaluate_ragas_jsonl.py
│   ├── export_ragas_dataset.py
│   └── fill_ground_truth_from_answers.py
├── config/                 # Configuration files
│   ├── __init__.py
│   ├── run_backend.py     # Backend startup script
│   └── requirements.txt   # Dependencies
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_utilities.py  # Utility tests
├── data/                   # Data files
├── chroma_db/             # Vector database
└── venv/                  # Virtual environment
```

## Key Features

- **Centralized Constants**: All configuration values are stored in `utilities/constants.py`
- **Modular Architecture**: Clear separation of concerns between API, frontend, and utilities
- **RAG Pipeline**: Complete retrieval-augmented generation workflow
- **Document Support**: PDF, DOCX, and HTML document processing
- **Vector Storage**: ChromaDB integration for document embeddings
- **Local LLM**: Ollama integration with Mistral model

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r config/requirements.txt
   ```

2. **Start Backend**:
   ```bash
   python config/run_backend.py
   ```

3. **Start Frontend**:
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

## Configuration

All configuration constants are centralized in `utilities/constants.py`:

- API settings (host, port, base URL)
- Model configuration (default model, embeddings)
- Document processing (chunk size, supported formats)
- Vector store settings (ChromaDB directory)
- Retriever parameters (k, fetch_k, lambda)
- LangChain prompts (contextualization, QA system prompts)



