from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
from utilities.chroma_utils import vectorstore
from utilities.constants import (
    RETRIEVER_K,
    RETRIEVER_FETCH_K,
    RETRIEVER_LAMBDA,
    DEFAULT_MODEL_NAME,
    CONTEXTUALIZE_Q_SYSTEM_PROMPT,
    QA_SYSTEM_PROMPT,
)

# Load environment variables from .env (LangSmith, model config, etc.)
load_dotenv()

# Tuned retriever: fewer finals, bigger candidate pool, balanced MMR
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": RETRIEVER_K,
        "fetch_k": RETRIEVER_FETCH_K,
        "lambda_mult": RETRIEVER_LAMBDA,
    },
)

output_parser = StrOutputParser()

# Set up prompts and chains using constants
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CONTEXTUALIZE_Q_SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# QA prompt with brevity and citation hints
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", QA_SYSTEM_PROMPT),
        ("system", "Context:\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)


def get_rag_chain(model: str = DEFAULT_MODEL_NAME):
    llm = ChatOllama(model=model)
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain
