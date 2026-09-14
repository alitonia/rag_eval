"""N3b: does the chunk-id-based conditioning match what the prompt actually
contained? (read-only)

For all 384 RAG answerable rows:
  full_in  : full normalized gold passage is a substring of the prompt
  prefix_in: first 80 normalized chars present
Cross-tab vs the round-3 scripts' chunk-id bucket (INTACT/TRUNCATED/ABSENT and
my GOLD_DROPPED split), then recompute the citation-unfaithful rates under the
TEXT-level definition to see if any paper number moves.
"""
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, ".")
from regrag.corpus.qa_loader import load_gold_questions  # noqa: E402
from regrag.evaluation.metrics import score_response  # noqa: E402
from regrag.models import GenerationResult  # noqa: E402


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip().lower()


golds = {q.id: q for q in load_gold_questions("data/gold/bank_qa_data.csv")}
qc = {q["id"]: q for q in json.load(open("data/gold/questions_canonical.json"))}
gen = json.load(open("data/eval/generations.json"))
meta = {json.loads(l)["cache_key"]: json.loads(l)
        for l in open("data/eval/generations_meta.jsonl")}
t1 = json.load(open("data/processed_chunks/tier1_chunks.json"))
t1_text = {c["chunk_id"]: norm(c["text"]) for c in t1}
qid2chunk = {}
for c in t1:
    md = c.get("metadata") or {}
    q = md.get("question_id") or ((md.get("question_ids") or [None])[0])
    if q:
        qid2chunk[q] = c["chunk_id"]

UNF = {"WRONG_INSTRUMENT", "NON_COVERING_PROVISION", "UNCITED_ASSERTION",
       "NUMERIC_THRESHOLD_MISMATCH"}

xtab = defaultdict(Counter)
text_bucket = {}          # cache_key -> TEXT-level bucket
rows_out = []
for g in gen:
    if g["retrieval_mode"] == "closed_book" or not golds[g["question_id"]].is_answerable:
        continue
    m = meta[g["cache_key"]]
    gp_full = norm(qc[g["question_id"]].get("gold_passage"))
    gp80 = gp_full[:80]
    prompt = norm(g["prompt"])
    full_in = bool(gp_full) and gp_full in prompt
    prefix_in = bool(gp80) and gp80 in prompt
    gold = qid2chunk.get(g["question_id"])
    ret = m.get("retrieved_chunk_ids") or []
    trr = m.get("rag_context_truncated_ranks") or []
    drr = m.get("rag_context_dropped_ranks") or []
    if gold is None or gold not in ret:
        cond = "ABSENT"
    elif ret.index(gold) + 1 in drr:
        cond = "GOLD_DROPPED"
    elif ret.index(gold) + 1 in trr:
        cond = "TRUNCATED"
    else:
        cond = "INTACT"
    tcond = "FULL" if full_in else ("PREFIX" if prefix_in else "NOTEXT")
    xtab[cond][tcond] += 1
    text_bucket[g["cache_key"]] = tcond
    if cond == "GOLD_DROPPED" and tcond != "FULL":
        rows_out.append((g["question_id"], g["model_name"], g["retrieval_mode"],
                         ret, drr, trr, tcond, len(gp_full)))

print("=== chunk-cond x text-level cross-tab (rows) ===")
for cond in ("INTACT", "TRUNCATED", "GOLD_DROPPED", "ABSENT"):
    print(f"{cond:12s}", dict(xtab[cond]))
print("\nGOLD_DROPPED rows without full text:")
for r in rows_out:
    print("  ", r)

# --- which sibling carries the text for GOLD_DROPPED rows, and is it clipped?
print("\n=== GOLD_DROPPED rows detail ===")
seen = set()
for g in gen:
    if g["retrieval_mode"] == "closed_book" or not golds[g["question_id"]].is_answerable:
        continue
    m = meta[g["cache_key"]]
    gold = qid2chunk.get(g["question_id"])
    ret = m.get("retrieved_chunk_ids") or []
    drr = m.get("rag_context_dropped_ranks") or []
    if gold in ret and ret.index(gold) + 1 in drr:
        key = (g["question_id"], g["retrieval_mode"])
        if key in seen:
            continue
        seen.add(key)
        prompt = norm(g["prompt"])
        gp_full = norm(qc[g["question_id"]].get("gold_passage"))
        trr = m.get("rag_context_truncated_ranks") or []
        sib = [(i + 1, cid, "TRUNC" if (i + 1) in trr else "ok",
                t1_text.get(cid, "?")[:40]) for i, cid in enumerate(ret)]
        print(f"{key} dropped_rank={drr} siblings={sib} goldfull_in_prompt={gp_full in prompt}")

# --- text-level conditioned unfaithful rates (rescore) ---
print("\n=== recompute unfaithful rates under TEXT-level buckets ===")
records = []
for g in gen:
    gr = GenerationResult(
        question_id=g["question_id"], model_name=g["model_name"],
        retrieval_mode=g["retrieval_mode"], prompt=g["prompt"],
        raw_response=g["raw_response"], answer_text=g["answer_text"],
        extracted_citations=g.get("extracted_citations", []),
        abstained=bool(g.get("abstained")), corpus_source=g.get("corpus_source", ""),
        retriever_backend=g.get("retriever_backend", ""), cache_key=g.get("cache_key", ""))
    s = score_response(gr, golds[g["question_id"]])
    records.append((g, set(s.hallucination_types)))

for mode in ("rag_bm25", "rag_dense"):
    for label, fn in (
        ("TEXT-FULL", lambda tb: tb == "FULL"),
        ("TEXT-PREFIX(non-full)", lambda tb: tb == "PREFIX"),
        ("TEXT-NOTEXT", lambda tb: tb == "NOTEXT"),
    ):
        sub = [(g, tp) for g, tp in records
               if g["retrieval_mode"] == mode and golds[g["question_id"]].is_answerable
               and fn(text_bucket[g["cache_key"]])]
        u = sum(1 for _, tp in sub if tp & UNF)
        n = len(sub)
        pct = f"{u/n*100:.1f}" if n else "-"
        print(f"{mode:9s} {label:22s} unfaithful {u:3d}/{n:3d} ({pct}%)")
