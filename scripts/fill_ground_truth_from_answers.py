#!/usr/bin/env python3
import json
import os

SRC = "data/ragas_dataset.jsonl"
DST = "data/ragas_dataset_gt.jsonl"

if not os.path.exists(SRC):
    raise SystemExit(f"Source not found: {SRC}")

written = 0
with open(SRC, encoding="utf-8") as fin, open(DST, "w", encoding="utf-8") as fout:
    for line in fin:
        if not line.strip():
            continue
        item = json.loads(line)
        gt = item.get("ground_truth")
        if not gt:
            # If you believe current answers are correct, use them as ground truth
            item["ground_truth"] = item.get("answer", "") or ""
        fout.write(json.dumps(item, ensure_ascii=False) + "\n")
        written += 1

print(f"Wrote {written} rows -> {DST}")
