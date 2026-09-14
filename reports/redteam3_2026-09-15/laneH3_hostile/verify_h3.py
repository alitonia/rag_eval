"""Lane H3 independent verification of paper claims (read-only).

Runs against repo data using the repo scorer exactly as compute_tables.py does,
then reports the specific numbers the paper asserts.
"""
import json, os, re, sys, unicodedata
from collections import Counter, defaultdict

REPO = "/mnt/data/seminar_2"
sys.path.insert(0, REPO)

from regrag.corpus.qa_loader import load_gold_questions
from regrag.evaluation.metrics import score_response, parse_notes
from regrag.models import GenerationResult

GOLD_CSV = os.path.join(REPO, "data", "gold", "bank_qa_data.csv")
UNFAITH = frozenset({"WRONG_INSTRUMENT", "NON_COVERING_PROVISION",
                     "UNCITED_ASSERTION", "NUMERIC_THRESHOLD_MISMATCH"})
CITE_ONLY = frozenset({"WRONG_INSTRUMENT", "NON_COVERING_PROVISION"})

golds = {q.id: q for q in load_gold_questions(GOLD_CSV)}
gens = json.load(open(os.path.join(REPO, "data", "eval", "generations.json")))
meta = {json.loads(l)["cache_key"]: json.loads(l)
        for l in open(os.path.join(REPO, "data", "eval", "generations_meta.jsonl"))}

print("gens rows:", len(gens), "meta rows:", len(meta))

records = {}
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
    rec = sc.to_record(corpus_source=gen.corpus_source, retriever_backend=gen.retriever_backend)
    rec._types = tuple(sc.hallucination_types)
    rec._notes = rec.notes or ""
    records[g["cache_key"]] = rec
    rec._gen = g

def show(label, value):
    print(f"== {label}: {value}")

# ---- RQ2 closed-book counts 102 / 76 ---------------------------------------
cb = [r for r in records.values() if r.retrieval_mode == "closed_book" and r.is_answerable]
n_wi = sum(1 for r in cb if set(r._types) & frozenset({"WRONG_INSTRUMENT"}))
n_nc = sum(1 for r in cb if set(r._types) & frozenset({"NON_COVERING_PROVISION"}))
n_unf = sum(1 for r in cb if set(r._types) & UNFAITH)
n_cite = sum(1 for r in cb if set(r._types) & CITE_ONLY)
types = Counter()
for r in cb:
    types.update(r._types)
show("closed-book answerable rows", len(cb))
show("unfaithful (4-type union)", n_unf)
show("WRONG_INSTRUMENT only", n_wi)
show("NON_COVERING only", n_nc)
show("cite-only union (WI|NC)", n_cite)
show("type counts closed-book", dict(types))

# ---- per-mode unfaithful vs cite-only vs UNCITED_ABS ------------------------
for mode in ("rag_bm25", "rag_dense", "closed_book"):
    rows = [r for r in records.values() if r.retrieval_mode == mode and r.is_answerable]
    u4 = sum(1 for r in rows if set(r._types) & UNFAITH)
    uwi = sum(1 for r in rows if set(r._types) & CITE_ONLY)
    uua = sum(1 for r in rows if set(r._types) & frozenset({"UNCITED_ASSERTION"}))
    tn = sum(1 for r in rows if set(r._types) & frozenset({"NUMERIC_THRESHOLD_MISMATCH"}))
    print(f"== {mode}: unfaith4={u4}/192 cite-only={uwi}/192 UNCITED_ASSERTION={uua} NUMERIC={tn}")

# ---- hedged then answered ---------------------------------------------------
hedged = [r for r in records.values() if "HEDGED_THEN_ANSWERED=1" in (r._notes or "")]
show("hedged-then-answered total (all modes)", len(hedged))
hed_cb = [r for r in hedged if r.retrieval_mode == "closed_book" and r.is_answerable]
show("hedged-then-answered closed-book answerable", len(hed_cb))
# breakdown by model/mode
by = Counter((r.model_name, r.retrieval_mode) for r in hedged)
show("hedged by model/mode", dict(by))

# ---- probe rows answered closed-book (claim 71/72) --------------------------
pb = [r for r in records.values() if r.retrieval_mode == "closed_book" and not r.is_answerable]
show("closed-book probe rows", len(pb))
show("closed-book probes abstained", sum(1 for r in pb if r.abstained))
show("closed-book probes answered", sum(1 for r in pb if not r.abstained))

# ---- identical answers 45/264 ----------------------------------------------
gkey = {(g["model_name"], g["retrieval_mode"], g["question_id"]): g for g in gens}
same = tot = 0
for qid, q in golds.items():
    for m in ("qwen-7b", "qwen-3b", "vistral-7b"):
        a = gkey[(m, "rag_bm25", qid)]["answer_text"]
        b = gkey[(m, "rag_dense", qid)]["answer_text"]
        tot += 1
        same += (a == b)
show("rag identical answers", f"{same}/{tot}")

# ---- finish reasons 709/83 --------------------------------------------------
fr = Counter(mt.get("finish_reason", "?") for mt in meta.values())
show("finish reasons", dict(fr))
stop = sum(1 for mt in meta.values() if mt.get("finish_reason") in ("stop", None))
trunc = sum(1 for mt in meta.values() if mt.get("finish_reason") == "length")
show("finish stop vs length", f"{stop}/{trunc}")

# ---- context budget 447/528, dropped 240, max chars -------------------------
rag_ctx = [mt for mt in meta.values() if "rag_context_chars" in mt]
tr = sum(1 for mt in rag_ctx if mt.get("rag_context_truncated_ranks"))
dr = sum(1 for mt in rag_ctx if mt.get("rag_context_dropped_ranks"))
mx = max(mt["rag_context_chars"] for mt in rag_ctx)
show("rag_context rows / truncated / dropped / max_chars", f"{len(rag_ctx)}/{tr}/{dr}/{mx}")

# ---- prompt_exact -----------------------------------------------------------
show("prompt_exact true", sum(1 for mt in meta.values() if mt.get("prompt_exact")))

# ---- evasion: how many truncated rows also have dropped? --------------------
both = sum(1 for mt in rag_ctx if mt.get("rag_context_truncated_ranks") and mt.get("rag_context_dropped_ranks"))
show("rows with both truncated and dropped", both)

# ---- per-row abstention flags sanity: abstained in generations.json ---------
ab = Counter((g["model_name"], g["retrieval_mode"], g["question_id"] in [q["id"] for q in []]) for g in [])
ga = [(g["model_name"], g["retrieval_mode"], bool(g.get("abstained"))) for g in gens]
ga_counts = Counter((m, mode) for m, mode, a in ga if a)
show("abstained flag by model/mode", dict(ga_counts))