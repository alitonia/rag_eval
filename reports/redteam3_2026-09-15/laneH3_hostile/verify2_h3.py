"""Lane H3 part 2: cite-only vs 4-type union inside conditioned cells + misc claims."""
import json, os, sys, unicodedata, re
from collections import Counter, defaultdict

REPO = "/mnt/data/seminar_2"
sys.path.insert(0, REPO)
from regrag.corpus.qa_loader import load_gold_questions
from regrag.evaluation.metrics import score_response
from regrag.models import GenerationResult

GOLD_CSV = os.path.join(REPO, "data", "gold", "bank_qa_data.csv")
CITE_ONLY = frozenset({"WRONG_INSTRUMENT", "NON_COVERING_PROVISION"})
UNFAITH = CITE_ONLY | frozenset({"UNCITED_ASSERTION", "NUMERIC_THRESHOLD_MISMATCH"})

golds = {q.id: q for q in load_gold_questions(GOLD_CSV)}
gens = json.load(open(os.path.join(REPO, "data", "eval", "generations.json")))
meta = {json.loads(l)["cache_key"]: json.loads(l)
        for l in open(os.path.join(REPO, "data", "eval", "generations_meta.jsonl"))}
t1 = json.load(open(os.path.join(REPO, "data", "processed_chunks", "tier1_chunks.json")))
qid2chunk = {}
for c in t1:
    md = c.get("metadata") or {}
    q = md.get("question_id") or (md.get("question_ids") or [None])[0]
    if q:
        qid2chunk[q] = c["chunk_id"]

# conditioning flags
cond = {}
for g in gens:
    if g["retrieval_mode"] == "closed_book":
        continue
    r = meta[g["cache_key"]]
    if not golds[g["question_id"]].is_answerable:
        continue
    gold = qid2chunk.get(g["question_id"])
    ret = r.get("retrieved_chunk_ids") or []
    tr = r.get("rag_context_truncated_ranks") or []
    if gold not in ret:
        c = "ABSENT"
    elif (ret.index(gold) + 1) in tr:
        c = "TRUNCATED"
    else:
        c = "INTACT"
    cond[(g["model_name"], g["retrieval_mode"], g["question_id"])] = c

records = []
for g in gens:
    gen = GenerationResult(
        question_id=g["question_id"], model_name=g["model_name"],
        retrieval_mode=g["retrieval_mode"], prompt=g["prompt"],
        raw_response=g["raw_response"], answer_text=g["answer_text"],
        extracted_citations=g.get("extracted_citations", []),
        abstained=bool(g.get("abstained")),
        corpus_source=g.get("corpus_source", ""),
        retriever_backend=g.get("retriever_backend", ""),
        cache_key=g.get("cache_key", ""))
    sc = score_response(gen, golds[g["question_id"]])
    rec = sc.to_record(corpus_source=gen.corpus_source,
                       retriever_backend=gen.retriever_backend)
    rec._types = tuple(sc.hallucination_types)
    records.append(rec)

print("=== conditioned cells: 4-type vs cite-only vs no-citation-only ===")
for mode in ("rag_bm25", "rag_dense"):
    rows = [r for r in records if r.retrieval_mode == mode and r.is_answerable]
    for c in ("ABSENT", "TRUNCATED", "INTACT"):
        sub = [r for r in rows if cond.get((r.model_name, r.retrieval_mode, r.question_id)) == c]
        u4 = sum(1 for r in sub if set(r._types) & UNFAITH)
        uc = sum(1 for r in sub if set(r._types) & CITE_ONLY)
        ua = sum(1 for r in sub if set(r._types) & frozenset({"UNCITED_ASSERTION"}))
        un = sum(1 for r in sub if set(r._types) & frozenset({"NUMERIC_THRESHOLD_MISMATCH"}))
        # rows where the ONLY unfaith type is UNCITED_ASSERTION (no citation at all)
        only_uncited = sum(1 for r in sub
                           if set(r._types) & UNFAITH and not (set(r._types) & CITE_ONLY))
        print(f"{mode:10s} {c:9s}: n={len(sub):3d} 4type={u4:3d} cite={uc:3d} "
              f"uncitedOnly={only_uncited:3d} (UA={ua}, NUM={un}) "
              f"4type%={u4/max(len(sub),1)*100:.1f} cite%={uc/max(len(sub),1)*100:.1f}")

print()
print("=== per-mode type union exclusivity ===")
for mode in ("rag_bm25", "rag_dense"):
    rows = [r for r in records if r.retrieval_mode == mode and r.is_answerable]
    uncited_only = sum(1 for r in rows
                       if set(r._types) & UNFAITH and not (set(r._types) & CITE_ONLY))
    num_only = sum(1 for r in rows
                   if set(r._types) & UNFAITH
                   and not (set(r._types) & CITE_ONLY)
                   and set(r._types) & frozenset({"NUMERIC_THRESHOLD_MISMATCH"}))
    print(f"{mode}: unfaith rows={sum(1 for r in rows if set(r._types) & UNFAITH)} "
          f"cite-only={sum(1 for r in rows if set(r._types) & CITE_ONLY)} "
          f"uncited-only={uncited_only} numeric-only-or-w={num_only}")

# ---- where do the 7B BM25 refused rows land (condition cells) ---------------
print()
print("=== refused (scorer) rows by condition, qwen-7b ===")
for mode in ("rag_bm25", "rag_dense"):
    for c in ("ABSENT", "TRUNCATED", "INTACT"):
        sub = [r for r in records
               if r.retrieval_mode == mode and r.is_answerable and r.abstained
               and cond.get((r.model_name, r.retrieval_mode, r.question_id)) == c]
        print(f"{mode:10s} {c:9s}: refused={len(sub)}")

# ---- answers of Q006 closed-book qwen-7b (paper example 1) ------------------
print()
print("=== Q006 closed_book qwen-7b: answer head + extracted citations ===")
for g in gens:
    if g["question_id"] == "Q006" and g["retrieval_mode"] == "closed_book" \
            and g["model_name"] == "qwen-7b":
        print("answer_text:", (g["answer_text"] or "")[:700])
        print("extracted_citations:", g.get("extracted_citations"))

# ---- Q008 closed-book sentinel + ND 02/2021 (paper example 2) ---------------
print()
print("=== Q008 closed_book: all models, sentinel present? ND02/2021 cited? ===")
for g in gens:
    if g["question_id"] == "Q008" and g["retrieval_mode"] == "closed_book":
        at = g["answer_text"] or ""
        print(g["model_name"], "| sentinel:", "không có trong kho văn bản" in at.lower(),
              "| nd02/2021:", "02/2021" in at, "| head:", at[:160].replace("\n", " "))

# ---- gold facts --------------------------------------------------------------
print()
print("=== gold facts ===")
qc = {q["id"]: q for q in json.load(open(os.path.join(REPO, "data", "gold", "questions_canonical.json")))}
print("Q006 gold:", {k: qc["Q006"].get(k) for k in
                     ("gold_doc_ids", "gold_citations", "doc_id_confidence")},
      "| passage head:", (qc["Q006"].get("gold_passage") or "")[:90])
print("Q036 gold:", {k: qc["Q036"].get(k) for k in
                     ("gold_doc_ids", "gold_citations", "doc_id_confidence", "notes")})
n_clause = sum(1 for q in qc.values() if q.get("is_answerable") and q.get("gold_citations")
               and q["gold_citations"][0].get("clause_id"))
print("answerable rows w/ clause gold:", n_clause)
print("total questions:", len(qc), "answerable:",
      sum(1 for q in qc.values() if q.get("is_answerable")))
# probe with capital-adequacy content
for q in qc.values():
    if not q.get("is_answerable"):
        t = ((q.get("question") or "") + " " + (q.get("gold_passage") or "")).lower()
        if "an toàn vốn" in t or "vốn tự có" in t or "capital" in t:
            print("probe capital-adequacy:", q["id"], "|",
                  (q.get("question") or "")[:110])

# extra: which answers on Q036 (annex) - no article gold - verify scorer cells
print("Q036 in canonical:", "Q036" in qc)

# ---- Tier-2 corpus size + instrument count -----------------------------------
print()
print("=== tier2 corpus ===")
import glob
t2_files = glob.glob(os.path.join(REPO, "data", "processed_chunks", "*.json"))
print("processed_chunks files:", [os.path.basename(f) for f in t2_files])