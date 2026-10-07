#!/usr/bin/env python3
"""Audit the external Vietnamese legal datasets under data/external/.

Answers three questions for the Q1 sequel's data-expansion plan:

1. SCHEMA  - what exactly did we download (row counts, fields, stated licenses)?
2. HARVEST - can regrag's own citation extractor turn ALQAC's free-text answers
   into (question -> instrument + article) candidate gold pairs? This is the
   "consultations as ground truth" idea tested on real data: a pair is only gold
   after human verification, but the harvest rate decides whether the track is
   worth staffing at all.
3. OVERLAP - do these dumps contain our own 88 benchmark questions? A containment
   hit would mean contamination (they must never be trained or validated on
   silently); it also tells us how close ALQAC/Zalo sit to our question
   distribution.

Read-only: writes nothing except the markdown report passed via --report.
Run:  .venv/bin/python scripts/audit_external_datasets.py --report reports/external_data_audit_2026-10-08.md
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from regrag.evaluation.citation import extract_citations  # noqa: E402

EXTERNAL = os.path.join(REPO_ROOT, "data", "external")
GOLD_CSV = os.path.join(REPO_ROOT, "data", "gold", "bank_qa_data.csv")


def norm(text: str) -> str:
    """Lowercase, collapse whitespace, strip diacritic-insensitive? No: keep
    diacritics (Vietnamese questions are comparable as-is after spacing only)."""
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def inventory(root: str) -> list:
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".cache"]
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            rows.append((os.path.relpath(path, root), os.path.getsize(path)))
    return rows


def audit_zalo(report: list) -> None:
    report.append("## Zalo 2021 (GreenNode mirror, MIT per card)\n")
    corpus_path = os.path.join(EXTERNAL, "zalo2021", "corpus.jsonl")
    docs, keys = [], None
    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            keys = keys or sorted(rec.keys())
            docs.append(rec)
    report.append(f"- corpus.jsonl: {len(docs)} docs, fields {keys}")
    lens = [len((d.get("text") or "")) for d in docs]
    report.append(f"- text chars: min {min(lens)}, median {sorted(lens)[len(lens)//2]}, max {max(lens)}")

    def count_jsonl(name):
        n = 0
        with open(os.path.join(EXTERNAL, "zalo2021", name), encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    n += 1
        return n

    report.append(f"- queries.jsonl: {count_jsonl('queries.jsonl')} queries")
    qrels = []
    for split in ("qrels/train.jsonl", "qrels/test.jsonl"):
        with open(os.path.join(EXTERNAL, "zalo2021", split), encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    qrels.append(json.loads(line))
    report.append(f"- qrels train+test: {len(qrels)} (fields {sorted(qrels[0].keys())})")

    # Harvest test: can the corpus doc text yield instrument+article pairs?
    paired = 0
    sample = docs[:500]
    for d in sample:
        blob = f"{d.get('title', '')}. {d.get('text', '')[:400]}"
        cits = extract_citations(blob)
        if any(c.get("doc_id") and c.get("article_id") for c in cits):
            paired += 1
    report.append(
        f"- harvest on 500 sampled corpus docs: {paired}/500 yield a "
        f"(document, article) pair via regrag citation extraction"
    )
    example = next((d for d in sample if d.get("title")), docs[0])
    report.append(
        f"- example doc (_id={example.get('_id')}): title={str(example.get('title'))[:100]!r} "
        f"text_head={str(example.get('text'))[:120]!r}"
    )


def audit_alqac(report: list) -> dict:
    report.append("\n## ALQAC 2024 dump (huyhuy123/ViLQA, research-only per card)\n")
    root = os.path.join(EXTERNAL, "alqac2024")
    parquets = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".cache"]
        parquets += [os.path.join(dirpath, f) for f in filenames if f.endswith(".parquet")]
    csvs = [os.path.join(root, f) for f in os.listdir(root) if f.endswith(".csv")]
    if parquets:
        import pyarrow.parquet as pq

        table = pq.read_table(parquets[0])
        rows = table.to_pylist()
        report.append(f"- parquet: {parquets[0]}, rows: {len(rows)}")
    elif csvs:
        with open(csvs[0], encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        report.append(f"- csv: {csvs[0]}, rows: {len(rows)}")
    else:
        report.append("- NO data file found")
        return {"questions": [], "n": 0}
    fields = sorted(rows[0].keys()) if rows else []
    report.append(f"- fields: {fields}")

    stats = Counter()
    paired_examples = []
    for r in rows:
        answer = r.get("Answer") or r.get("answer") or ""
        question = r.get("Question") or r.get("question") or ""
        if not isinstance(answer, str):
            answer = str(answer)
        cits = extract_citations(answer)
        has_doc = any(c.get("doc_id") for c in cits)
        has_pair = any(c.get("doc_id") and c.get("article_id") for c in cits)
        stats["answers"] += 1
        stats["with_any_citation"] += bool(cits)
        stats["with_instrument"] += has_doc
        stats["with_instrument_and_article"] += has_pair
        if has_pair and len(paired_examples) < 3:
            best = next(c for c in cits if c.get("doc_id") and c.get("article_id"))
            paired_examples.append((str(question)[:90], best.get("doc_id"), best.get("article_id")))
    n = max(stats["answers"], 1)
    report.append(
        f"- citation harvest over ALL {n} answers: "
        f"{stats['with_any_citation']} ({stats['with_any_citation']*100//n}%) carry any citation, "
        f"{stats['with_instrument']} ({stats['with_instrument']*100//n}%) name an instrument, "
        f"{stats['with_instrument_and_article']} ({stats['with_instrument_and_article']*100//n}%) yield a "
        f"(instrument, article) pair = candidate gold pending human verification"
    )
    for q, doc, art in paired_examples:
        report.append(f"  - e.g. Q={q!r} -> {doc} / Điều {art}")
    return {"questions": [norm(r.get("Question", "")) for r in rows], "n": len(rows)}


def audit_vibidlqa(report: list) -> None:
    report.append("\n## ViBidLQA (ntphuc149, Apache-2.0 per card)\n")
    root = os.path.join(EXTERNAL, "vibidlqa")
    for rel, size in inventory(root):
        report.append(f"- {rel} ({size} bytes)")
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if name.endswith(".jsonl"):
            with open(path, encoding="utf-8") as f:
                first = f.readline().strip()
                n = 1 + sum(1 for line in f if line.strip())
            rec = json.loads(first)
            report.append(f"- {name}: {n} rows, fields {sorted(rec.keys())}")
            report.append(f"  sample: {json.dumps(rec, ensure_ascii=False)[:220]}")
        elif name.endswith(".csv"):
            with open(path, encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            report.append(f"- {name}: {len(rows)} rows, fields {sorted(rows[0].keys()) if rows else []}")


def overlap_check(report: list, alqac: dict) -> None:
    report.append("\n## Contamination check vs our 88 benchmark questions\n")
    with open(GOLD_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        qcol = next((c for c in reader.fieldnames if "question" in c.lower()), reader.fieldnames[0])
        ours = [norm(r.get(qcol, "")) for r in reader if r.get(qcol)]
    alqac_set = set(alqac["questions"])
    zalo_queries = []
    qpath = os.path.join(EXTERNAL, "zalo2021", "queries.jsonl")
    if os.path.exists(qpath):
        with open(qpath, encoding="utf-8") as f:
            zalo_queries = [norm(json.loads(line).get("text", "")) for line in f if line.strip()]
    zalo_set = set(zalo_queries)
    hits_alqac = [q for q in ours if q in alqac_set]
    hits_zalo = [q for q in ours if q in zalo_set]
    report.append(f"- our questions exactly contained in ALQAC dump: {len(hits_alqac)}/{len(ours)}")
    report.append(f"- our questions exactly contained in Zalo queries: {len(hits_zalo)}/{len(ours)}")
    if hits_alqac:
        report.append(f"  - e.g. {hits_alqac[0][:90]!r}")
    if hits_zalo:
        report.append(f"  - e.g. {hits_zalo[0][:90]!r}")
    report.append(
        "- exact-match containment only; near-duplicates are NOT covered by this check, "
        "so any future training use of these dumps still needs an embedding-level dedup pass"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--report", help="write the markdown report here")
    args = ap.parse_args()

    report = ["# External dataset audit — 2026-10-08\n"]
    report.append("## Files on disk\n")
    for root_name in ("zalo2021", "alqac2024", "vibidlqa"):
        root = os.path.join(EXTERNAL, root_name)
        if os.path.isdir(root):
            for rel, size in inventory(root):
                report.append(f"- `{root_name}/{rel}` ({size:,} bytes)")
    audit_zalo(report)
    alqac = audit_alqac(report)
    audit_vibidlqa(report)
    overlap_check(report, alqac)
    text = "\n".join(report) + "\n"
    print(text)
    if args.report:
        os.makedirs(os.path.dirname(args.report), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\nreport -> {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
