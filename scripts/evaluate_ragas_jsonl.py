import json
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
import os
from utilities.constants import DEFAULT_MODEL_NAME, EMBEDDING_MODEL_NAME

# Configure your local Ollama endpoint if non-default
# os.environ.setdefault("OLLAMA_HOST", "http://localhost:11434")

# Load JSONL
rows = [json.loads(l) for l in open("data/ragas_dataset_gt.jsonl", encoding="utf-8")]
# Keep only rows with minimum fields
rows = [
    r
    for r in rows
    if r.get("question")
    and r.get("answer") is not None
    and r.get("contexts") is not None
]
print("rows-------", rows)

# Build dataset
ds = Dataset.from_list(
    [
        {
            "question": r["question"],
            "answer": r["answer"],
            "contexts": r.get("contexts", []),
            "ground_truth": r.get("ground_truth", ""),
        }
        for r in rows
    ]
)
print("ds-------", ds)

# Choose metrics
metrics = [faithfulness, answer_relevancy, context_precision, context_recall]
if any(r.get("ground_truth") for r in rows):
    metrics.append(context_recall)

# Use local Ollama model (ensure it's available: `ollama pull {DEFAULT_MODEL_NAME}`)
llm = ChatOllama(model=DEFAULT_MODEL_NAME)

# Local embeddings via HuggingFace (no OpenAI key needed)
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

result = evaluate(ds, metrics=metrics, llm=llm, embeddings=embeddings)
print(result)
print(result.to_pandas().head())
