"""Lane N3 independent spot-checks (read-only). Repo-root cwd required.

Re-derives, independently of the round-3 scripts:
  A. meta: RAG rows, truncated rows, dropped rows, SUM of dropped ranks (passage
     count), max/mean rag_context_chars, finish reasons
  B. tier1 chunk count (64-chunk fixture claim)
  C. row-level conditioning counts + per-question gold-in-top3 counts
  D. hedge-then-answer on closed-book rows: answerable-only (80?), probes (35?),
     plus exact-tier-only variant
  E. identical answers between RAG arms (45/264?)
  F. Q006 vistral-7b rag_bm25: conditioning, gold text in prompt, answer
     opening, scorer verdict, correctness
  G. closed-book probe abstentions (1/72 -> "71 of 72")
  H. closed-book answerable unfaithful types (102 NCP, 76 WI) + 94/83 RAG
  I. false refusals 16/15/10/4 and rates
"""
import json
import sys
from collections import Counter, defaultdict

sys.path.insert(0, ".")
from regrag.corpus.qa_loader import load_gold_questions  # noqa: E402
from regrag.evaluation.metrics import score_response  # noqa: E402
from regrag.models import GenerationResult  # noqa: E402

gen = json.load(open("data/eval/generations.json"))
meta = {json.loads(l)["cache_key"]: json.loads(l)
        for l in open("data/eval/generations_meta.jsonl")}
t1 = json.load(open("data/processed_chunks/tier1_chunks.json"))
qc = {q["id"]: q for q in json.load(open("data/gold/questions_canonical.json"))}
golds = {q.id: q for q in load_gold_questions("data/gold/bank_qa_data.csv")}

print("=== A. meta / context budget ===")
rag = [m for m in meta.values() if m["retrieval_mode"] != "closed_book"]
print("RAG rows:", len(rag))
tr_rows = [m for m in rag if m.get("rag_context_truncated_ranks")]
dr_rows = [m for m in rag if m.get("rag_context_dropped_ranks")]
dr_pass = sum(len(m.get("rag_context_dropped_ranks") or []) for m in rag)
tr_pass = sum(len(m.get("rag_context_truncated_ranks") or []) for m in rag)
print("rows w/ truncated ranks:", len(tr_rows), "| total truncated passages:", tr_pass)
print("rows w/ dropped ranks:", len(dr_rows), "| TOTAL DROPPED PASSAGES:", dr_pass)
for m in dr_rows[:6]:
    print("   drop example:", m["question_id"], m["model_name"],
          "dropped=", m.get("rag_context_dropped_ranks"),
          "trunc=", m.get("rag_context_truncated_ranks"),
          "chars=", m.get("rag_context_chars"))
chars = [m["rag_context_chars"] for m in rag if "rag_context_chars" in m]
print("context chars: max", max(chars), "mean", round(sum(chars)/len(chars), 2), "n", len(chars))
fr = Counter(m.get("finish_reason") for m in meta.values())
print("finish reasons:", dict(fr))
budgets = {m.get("rag_context_budget") for m in rag if "rag_context_budget" in m}
print("stamped budgets:", budgets)

print("=== B. tier1 fixture size ===")
print("tier1 chunks:", len(t1))

print("=== C. conditioning counts (independent) ===")
qid2chunk = {}
for c in t1:
    md = c.get("metadata") or {}
    q = md.get("question_id") or ((md.get("question_ids") or [None])[0])
    if q:
        qid2chunk[q] = c["chunk_id"]
stats = defaultdict(Counter)
per_q = defaultdict(set)
for m in rag:
    if not m.get("is_answerable"):
        continue
    g = qid2chunk.get(m["question_id"])
    ret = m.get("retrieved_chunk_ids") or []
    trr = m.get("rag_context_truncated_ranks") or []
    drr = m.get("rag_context_dropped_ranks") or []
    if g is None or g not in ret:
        cond = "ABSENT"
    elif ret.index(g) + 1 in drr:
        cond = "GOLD_DROPPED"
    elif ret.index(g) + 1 in trr:
        cond = "TRUNCATED"
    else:
        cond = "INTACT"
    stats[m["retrieval_mode"]][cond] += 1
    if cond in ("INTACT", "TRUNCATED"):
        per_q[m["retrieval_mode"]].add(m["question_id"])
for mode, c in sorted(stats.items()):
    print(mode, dict(c), "total", sum(c.values()))
for mode, qs in sorted(per_q.items()):
    print(mode, "questions with gold in top3:", len(qs))

print("=== D. hedge-then-answer (closed-book) ===")
hedge_ans = hedge_probe = hedge_exact_ans = 0
for g in gen:
    if g["retrieval_mode"] != "closed_book":
        continue
    gold = golds[g["question_id"]]
    gr = GenerationResult(
        question_id=g["question_id"], model_name=g["model_name"],
        retrieval_mode=g["retrieval_mode"], prompt=g["prompt"],
        raw_response=g["raw_response"], answer_text=g["answer_text"],
        extracted_citations=g.get("extracted_citations", []),
        abstained=bool(g.get("abstained")), corpus_source=g.get("corpus_source", ""),
        retriever_backend=g.get("retriever_backend", ""), cache_key=g.get("cache_key", ""))
    s = score_response(gr, gold)
    hedged = s.abstention.hedged_then_answered
    exact = bool(s.abstention.matched)
    if gold.is_answerable:
        hedge_ans += bool(hedged)
        hedge_exact_ans += bool(hedged and exact)
    else:
        hedge_probe += bool(hedged)
print("hedged answerable:", hedge_ans, "| hedged probes:", hedge_probe,
      "| hedged answerable w/ EXACT sentinel:", hedge_exact_ans)

print("=== E. identical RAG-arm answers ===")
gens_by_key = {(g["model_name"], g["retrieval_mode"], g["question_id"]): g for g in gen}
ident = tot = 0
for qid in golds:
    for m in ("qwen-3b", "qwen-7b", "vistral-7b"):
        a = gens_by_key[(m, "rag_bm25", qid)]["answer_text"]
        b = gens_by_key[(m, "rag_dense", qid)]["answer_text"]
        tot += 1
        ident += (a == b)
print("identical:", ident, "of", tot)

print("=== F. Q006 vistral-7b rag_bm25 ===")
import re as _re
import unicodedata
def norm(s):
    return _re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip().lower()
g6 = gens_by_key[("vistral-7b", "rag_bm25", "Q006")]
m6 = meta[g6["cache_key"]]
gold = golds["Q006"]
gp = norm(qc["Q006"].get("gold_passage") or "")[:80]
print("gold passage[:80]:", gp)
print("gold passage in prompt:", gp in norm(g6["prompt"]))
print("answer_text[:200]:", norm(g6["answer_text"])[:200])
print("extracted:", g6.get("extracted_citations"))
gr = GenerationResult(
    question_id="Q006", model_name="vistral-7b", retrieval_mode="rag_bm25",
    prompt=g6["prompt"], raw_response=g6["raw_response"], answer_text=g6["answer_text"],
    extracted_citations=g6.get("extracted_citations", []),
    abstained=bool(g6.get("abstained")), corpus_source=g6.get("corpus_source", ""),
    retriever_backend=g6.get("retriever_backend", ""), cache_key=g6.get("cache_key", ""))
s6 = score_response(gr, gold)
print("correctness:", s6.correctness_score, "abstained:", s6.abstention.abstained,
      "types:", sorted(set(s6.hallucination_types)))
ret6 = m6.get("retrieved_chunk_ids") or []
tr6 = m6.get("rag_context_truncated_ranks") or []
dr6 = m6.get("rag_context_dropped_ranks") or []
print("retrieved:", ret6, "trunc:", tr6, "dropped:", dr6,
      "gold_chunk:", qid2chunk.get("Q006"), "-> cond:",
      ("ABSENT" if qid2chunk.get("Q006") not in ret6 else
       "DROPPED" if ret6.index(qid2chunk["Q006"])+1 in dr6 else
       "TRUNC" if ret6.index(qid2chunk["Q006"])+1 in tr6 else "INTACT"))

print("=== G. closed-book probes abstaining ===")
ab = sum(1 for g in gen if g["retrieval_mode"] == "closed_book"
         and not golds[g["question_id"]].is_answerable and g.get("abstained"))
print("closed-book probe abstentions:", ab, "of 72")

print("=== H. closed-book unfaithful types + RAG gate ===")
UNF = {"WRONG_INSTRUMENT", "NON_COVERING_PROVISION", "UNCITED_ASSERTION",
       "NUMERIC_THRESHOLD_MISMATCH"}
cnt = defaultdict(Counter)
for g in gen:
    if not golds[g["question_id"]].is_answerable:
        continue
    gr = GenerationResult(
        question_id=g["question_id"], model_name=g["model_name"],
        retrieval_mode=g["retrieval_mode"], prompt=g["prompt"],
        raw_response=g["raw_response"], answer_text=g["answer_text"],
        extracted_citations=g.get("extracted_citations", []),
        abstained=bool(g.get("abstained")), corpus_source=g.get("corpus_source", ""),
        retriever_backend=g.get("retriever_backend", ""), cache_key=g.get("cache_key", ""))
    s = score_response(gr, golds[g["question_id"]])
    tp = set(s.hallucination_types)
    cnt[g["retrieval_mode"]]["NCP"] += ("NON_COVERING_PROVISION" in tp)
    cnt[g["retrieval_mode"]]["WI"] += ("WRONG_INSTRUMENT" in tp)
    cnt[g["retrieval_mode"]]["UNF"] += bool(tp & UNF)
for mode, c in sorted(cnt.items()):
    print(mode, dict(c))
