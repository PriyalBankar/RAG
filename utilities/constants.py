# Shared constants and configuration

# ============================================================================
# API Configuration
# ============================================================================
API_HOST = "0.0.0.0"
API_PORT = 8000
API_BASE_URL = "http://localhost:8000"

# ============================================================================
# Model Configuration
# ============================================================================
DEFAULT_MODEL_NAME = "mistral:7b-instruct-q4_0"

# ============================================================================
# Retriever Parameters
# ============================================================================
RETRIEVER_K = 3
RETRIEVER_FETCH_K = 40
RETRIEVER_LAMBDA = 0.6

# ============================================================================
# Document Processing
# ============================================================================
# Chunking parameters
CHUNK_SIZE = 700
CHUNK_OVERLAP = 120
MIN_CHUNK_CHARS = 60

# Supported file extensions
SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".html"]
SUPPORTED_EXTENSIONS_WITHOUT_DOT = ["pdf", "docx", "html"]

# ============================================================================
# Embeddings and Vector Store
# ============================================================================
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L12-v2"
CHROMA_DIR = "./chroma_db"

# ============================================================================
# File Processing
# ============================================================================
TEMP_FILE_PREFIX = "temp_"

# ============================================================================
# Greeting Messages
# ============================================================================
GREETING_MESSAGES = ["hi", "hello", "hey", "hi!", "hello!", "hey!"]
DEFAULT_GREETING_RESPONSE = (
    "Hi! I'm your RAG assistant. Ask a question about your uploaded documents."
)

# ============================================================================
# LangChain Prompts
# ============================================================================
# Contextualize question system prompt
CONTEXTUALIZE_Q_SYSTEM_PROMPT = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

# QA system prompt
QA_SYSTEM_PROMPT = (
    "You are a careful, concise assistant for question answering.\n"
    "You must answer ONLY using the provided context.\n"
    "If the answer is not fully contained in the context, reply exactly: 'I don't know.'\n"
    "Do not fabricate facts. Do not use outside knowledge.\n"
    "Start by restating the question in a few words, then answer in 1-2 sentences.\n"
    "When relevant, include a short quoted snippet from the context."
)
