from fastapi import FastAPI, File, UploadFile, HTTPException
from .pydantic_models import QueryInput, QueryResponse, DocumentInfo
from utilities.langchain_utils import get_rag_chain
from utilities.constants import (
    DEFAULT_MODEL_NAME,
    SUPPORTED_EXTENSIONS,
    GREETING_MESSAGES,
    DEFAULT_GREETING_RESPONSE,
    TEMP_FILE_PREFIX,
)
from utilities.db import (
    insert_application_logs,
    get_chat_history,
    get_all_documents,
    insert_document_record,
)
from utilities.chroma_utils import index_document_to_chroma
import uuid
import logging
import time
from dotenv import load_dotenv
import os

import shutil

# Load environment variables from .env so LangSmith and other configs are available
load_dotenv()

logging.basicConfig(filename="app.log", level=logging.INFO)
app = FastAPI()


@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id
    question = (query_input.question or "").strip()
    logging.info(
        f"Session ID: {session_id}, User Query: {question}, Model: {query_input.model.value}"
    )
    if not session_id:
        session_id = str(uuid.uuid4())

    lower_q = question.lower()
    if lower_q in GREETING_MESSAGES:
        answer = DEFAULT_GREETING_RESPONSE
        insert_application_logs(
            session_id, question, answer, query_input.model.value, 0.0
        )
        logging.info(f"Session ID: {session_id}, AI Response: {answer}")
        return QueryResponse(
            answer=answer, session_id=session_id, model=query_input.model
        )

    chat_history = get_chat_history(session_id)
    rag_chain = get_rag_chain(
        query_input.model.value
        if hasattr(query_input.model, "value")
        else DEFAULT_MODEL_NAME
    )

    t0 = time.perf_counter()
    result = rag_chain.invoke({"input": question, "chat_history": chat_history})
    latency_s = time.perf_counter() - t0
    latency_s = round(latency_s, 2)

    context_docs = result.get("context", []) if isinstance(result, dict) else []
    answer = result.get("answer") if isinstance(result, dict) else None
    
    # Extract reasoning information
    reasoning = ""
    sources = []
    confidence = 0.0
    
    if context_docs:
        # Extract source information
        sources = [doc.metadata.get("source", "Unknown") if hasattr(doc, 'metadata') else "Unknown" 
                  for doc in context_docs]
        
        # Parse reasoning from model response if available
        if answer and "REASONING:" in answer:
            # Split response to extract reasoning and answer
            parts = answer.split("ANSWER:", 1)
            if len(parts) == 2:
                reasoning_part = parts[0].replace("REASONING:", "").strip()
                answer = parts[1].strip()
                reasoning = reasoning_part
            else:
                reasoning = f"Based on {len(context_docs)} relevant document(s): {', '.join(sources)}. "
                reasoning += f"The answer was constructed using the most relevant information from these sources."
        else:
            # Generate reasoning based on context
            reasoning = f"Based on {len(context_docs)} relevant document(s): {', '.join(sources)}. "
            reasoning += f"The answer was constructed using the most relevant information from these sources."
        
        # Simple confidence scoring based on context relevance
        confidence = min(0.9, 0.5 + (len(context_docs) * 0.1))
    else:
        answer = (
            answer if answer and "don't know" in answer.lower() else "I don't know."
        )
        reasoning = "No relevant documents found in the knowledge base."
        confidence = 0.1

    insert_application_logs(
        session_id, question, answer, query_input.model.value, latency_s
    )
    logging.info(
        f"Session ID: {session_id}, Latency: {latency_s:.2f} s, AI Response: {answer}"
    )
    
    return QueryResponse(
        answer=answer, 
        session_id=session_id, 
        model=query_input.model,
        reasoning=reasoning,
        sources=sources,
        confidence=confidence
    )




@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    allowed_extensions = SUPPORTED_EXTENSIONS
    file_extension = os.path.splitext(file.filename)[1].lower()
    print('file_extension-------',file_extension)

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed types are: {', '.join(allowed_extensions)}",
        )

    temp_file_path = f"{TEMP_FILE_PREFIX}{file.filename}"
    print('--------temp_file_path-------',temp_file_path)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_id = insert_document_record(file.filename)
        success = index_document_to_chroma(temp_file_path, file_id)

        if success:
            return {
                "message": f"File {file.filename} has been successfully uploaded and indexed.",
                "file_id": file_id,
            }
        # else: keep record for debugging if indexing fails
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@app.get("/list-docs", response_model=list[DocumentInfo])
def list_documents():
    return get_all_documents()
