from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
import os
from .constants import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    MIN_CHUNK_CHARS,
    EMBEDDING_MODEL_NAME,
    CHROMA_DIR,
    SUPPORTED_EXTENSIONS,
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
)

embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
vectorstore = Chroma(
    persist_directory=CHROMA_DIR, embedding_function=embedding_function
)


def load_and_split_document(file_path: str) -> List[Document]:
    if file_path.endswith(SUPPORTED_EXTENSIONS[0]):  # .pdf
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(SUPPORTED_EXTENSIONS[1]):  # .docx
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith(SUPPORTED_EXTENSIONS[2]):  # .html
        loader = UnstructuredHTMLLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    documents = loader.load()
    return text_splitter.split_documents(documents)


def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        splits = load_and_split_document(file_path)
        # Basic quality filter: skip very short/boilerplate chunks; dedupe exact texts
        seen_texts = set()
        filtered: List[Document] = []
        for split in splits:
            text = (split.page_content or "").strip()
            if len(text) < MIN_CHUNK_CHARS:
                continue
            if text in seen_texts:
                continue
            seen_texts.add(text)
            split.metadata["file_id"] = file_id
            filtered.append(split)
        if not filtered:
            return False
        vectorstore.add_documents(filtered)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False
