#!/usr/bin/env python3
import os
import sys
import json
import sqlite3
from typing import List, Dict

# Ensure we can import from the local package (api)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
print("-------", PROJECT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Lazy import after sys.path tweak
from utilities.chroma_utils import vectorstore


def get_recent_logs(db_path: str, limit: int = 50) -> List[Dict]:
    if not os.path.exists(db_path):
        return []
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, session_id, user_query AS question, gpt_response AS answer
        FROM application_logs
        WHERE COALESCE(TRIM(user_query), '') <> ''
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def retrieve_contexts(questions: List[str], k: int = 4) -> List[List[str]]:
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
    contexts: List[List[str]] = []
    for q in questions:
        try:
            docs = retriever.get_relevant_documents(q)
            contexts.append([d.page_content for d in docs])
        except Exception:
            contexts.append([])
    return contexts


def main():
    out_dir = os.path.join(PROJECT_ROOT, "data")
    print("out_dir-------", out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "ragas_dataset.jsonl")
    print("out_path-------", out_path)
    db_path = os.path.join(PROJECT_ROOT, "rag_app.db")
    print("db_path-------", db_path)
    logs = get_recent_logs(db_path, limit=100)
    print("logs-------", logs)
    if not logs:
        print("No logs found. Make sure the backend has been used and logs exist.")
        return

    questions = [r["question"] for r in logs]
    answers = [r["answer"] for r in logs]

    contexts_list = retrieve_contexts(questions, k=4)
    print("-------", contexts_list)

    written = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for question, answer, contexts in zip(questions, answers, contexts_list):
            item = {
                "question": question or "",
                "answer": answer or "",
                "contexts": contexts or [],
                # Fill ground truth later; for now keep empty
                "ground_truth": "",
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            written += 1

    print(f"Wrote {written} samples to {out_path}")


if __name__ == "__main__":
    main()
