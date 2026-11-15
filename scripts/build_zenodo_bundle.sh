#!/usr/bin/env bash
# build_zenodo_bundle.sh — assemble the public Zenodo deposit bundle from git HEAD.
#
# The bundle ships an explicit allowlist of tracked files, never the whole
# tree: internal working documents (reports/, docs/, notebooks/, ops archives,
# dataset-discovery one-offs) stay out of the deposit. The bundle is built
# ONLY from tracked files at HEAD (git archive), so what goes to Zenodo is
# exactly what is committed — never a dirty working tree. The raw ingested
# sources are gitignored (the manifest carries URL+sha1 provenance) and are
# copied from the working tree, pinned by DOC_MANIFEST.json sha1s.
#
# Usage: bash scripts/build_zenodo_bundle.sh [output-dir]
# Output: <output-dir>/regrag-vn-rivf2026/ + SHA256SUMS, size printed.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT="${1:-dist/zenodo_bundle}"
NAME="regrag-vn-rivf2026"

# Refuse a dirty tree: the DOI must point at exactly one commit state.
# Untracked files (scratch dirs) never enter git archive, so they don't count.
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  echo "[FATAL] working tree has modified tracked files — commit or stash first:" >&2
  git status --porcelain --untracked-files=no >&2 | head -10
  exit 1
fi

COMMIT="$(git rev-parse --short HEAD)"
rm -rf "$OUT"
mkdir -p "$OUT"

# Public allowlist: benchmark code and data, campaign logs, paper.
# scripts/ is enumerated file-by-file: one-off discovery, blind-review and
# release-tooling scripts stay out of the deposit.
TRACKS=(
  README.md
  LICENSE
  requirements.txt
  regrag/
  tests/
  paper/main.tex paper/main.pdf paper/refs.bib paper/vnchars.sty
  paper/IEEEtran.cls paper/IEEEtran.bst
  scripts/load_qa_csv.py
  scripts/build_corpus_chunks.py
  scripts/build_tier1_corpus.py
  scripts/regenerate.py
  scripts/repair_gold_passages.py
  scripts/audit_gold_passages.py
  scripts/eval_bm25_recall.py
  scripts/compute_tables.py
  scripts/compute_conditioned_rates.py
  scripts/verify_tier1_conditioning.py
  scripts/run_eval.py
  scripts/run_campaign_pod.py
  scripts/preflight_memory.py
  scripts/enrich_meta_rag_context.py
  scripts/build_human_label_sets.py
  scripts/analyze_scorer_validation.py
  scripts/pod_run_campaign.sh
  scripts/pod_fetch_campaign.sh
  scripts/pod_cleanup.sh
  scripts/pod_hf_push_campaign.sh
  scripts/pod_run_dense_gate_c.sh
  data/gold/bank_qa_data.csv
  data/gold/questions_canonical.json
  data/gold/citation_overrides.json
  data/gold/passage_repair_log.json
  data/gold/TT61_TRIPLE_FINDINGS.md
  data/processed_chunks/
  data/human/scorer_validation_50.csv
  data/human/VALIDATION_INSTRUCTIONS.md
  data/human/scorer_validation_sample_2026-09-13.json
  data/eval/bm25_recall_gate_c_2026-09-11.json
  data/eval/bm25_recall_gate_c_2026-11-16-goldfix.json
  data/eval/dense_recall_gate_c_2026-09-13.json
  data/eval/generations.json
  data/eval/generations_meta.jsonl
  data/eval/scorer_validation_2026-09-15.json
  data/eval/conditioned_rates_2026-11-16-goldfix.txt
  data/eval/tables_paper_2026-09-13.json
  data/eval/tables_paper_2026-11-16-goldfix.json
)

tar_list="$(mktemp)"
trap 'rm -f "$tar_list"' EXIT
for t in "${TRACKS[@]}"; do
  if ! git ls-files -- "$t" | grep .; then
    echo "[FATAL] allowlist path is not tracked (commit it or drop it): $t" >&2
    exit 1
  fi
  git ls-files -- "$t" >> "$tar_list"
done

git archive --format=tar.gz --prefix="$NAME/" --pathspec-from-file="$tar_list" \
  -o "$OUT/$NAME-$COMMIT.tar.gz"

# Also lay the tree out unpacked for Zenodo's web UI (which shows archives
# poorly): same content, plain files.
mkdir -p "$OUT/$NAME"
git archive --format=tar --prefix="$NAME/" --pathspec-from-file="$tar_list" \
  | tar xf - -C "$OUT"

# The raw ingested sources are gitignored (repo policy: manifest carries
# URL+sha1 provenance), but the paper's Data and Code Availability paragraph
# promises "legal texts redistributed as downloaded" — so the deposit includes
# them from the working tree, pinned by DOC_MANIFEST.json sha1s.
cp -r data/raw_legal "$OUT/$NAME/data/raw_legal"

( cd "$OUT/$NAME" && find . -type f -exec sha256sum {} \; ) > "$OUT/SHA256SUMS.txt"

SIZE=$(du -sh "$OUT" | cut -f1)
echo "[OK] bundle at $OUT (commit $COMMIT, $SIZE)"
echo "     archive: $OUT/$NAME-$COMMIT.tar.gz"
echo "     tree:    $OUT/$NAME/"
echo "     next:    bash scripts/zenodo_deposit.sh $OUT/$NAME   (needs ZENODO_ACCESS_TOKEN; run manually when the owner says so)"
