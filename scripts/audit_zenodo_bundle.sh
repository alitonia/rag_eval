#!/usr/bin/env bash
# audit_zenodo_bundle.sh — leak battery + replay gate for the Zenodo deposit.
#
# Gates (each judged on its own; every hit is adjudicated, never averaged):
#   G0 battery calibration — the sweep must FIRE on a synthetic control tree
#     planted with every banned pattern, so a silent zero can never pass
#     as clean.
#   G1 internal-vocabulary sweep — pod session names, machine paths, process
#     vocabulary (audit lanes, rounds, EDAS, boards, camera-ready).
#   G2 exclusion check — internal dirs and one-off artifacts absent from the
#     shipped tree.
#   G3 replay gate — recompute Tables I/II from the shipped campaign log with
#     the shipped scorer and shipped gold, value-identical to the shipped
#     tables JSON. The interpreter comes from the repo venv (dependency
#     install is requirements.txt's job); the DATA and CODE come from the
#     unpacked bundle alone.
#   G4 integrity — SHA256SUMS matches the shipped tree.
#
# Usage: bash scripts/audit_zenodo_bundle.sh [bundle-dir] [sha-file]
#   bundle-dir defaults to dist/zenodo_bundle/regrag-vn-rivf2026
#   sha-file    defaults to dist/zenodo_bundle/SHA256SUMS.txt
set -euo pipefail
cd "$(dirname "$0")/.."

BUNDLE="${1:-dist/zenodo_bundle/regrag-vn-rivf2026}"
SHAFILE="${2:-dist/zenodo_bundle/SHA256SUMS.txt}"
PY=".venv/bin/python"
fail=0

[ -d "$BUNDLE" ] || { echo "[FATAL] bundle not found: $BUNDLE (run scripts/build_zenodo_bundle.sh first)"; exit 1; }
[ -f "$SHAFILE" ] || { echo "[FATAL] checksum file not found: $SHAFILE"; exit 1; }

CTRL="$(mktemp -d)"
REPLAY="$(mktemp -d)"
trap 'rm -rf "$CTRL" "$REPLAY"' EXIT

# --- G0: battery calibration ---------------------------------------------------
mkdir -p "$CTRL/depth/probe"
printf 'pod zesty_coffee_herring and clumsy_pink_chimpanzee here\n' > "$CTRL/depth/probe/a.txt"
printf 'see /mnt/data/seminar_2/reports and /home/alitonia/x\n' > "$CTRL/depth/probe/b.txt"
printf 'red-team laneH2 laneN3 laneW2 round-2 finding; upload to EDAS before camera-ready; see KANBAN and PROJECT_PLAN; blind-rank venue-rank\n' > "$CTRL/depth/probe/c.txt"
c_hits=$(grep -rliE "zesty_coffee_herring|clumsy_pink_chimpanzee|/mnt/data|/home/alitonia|red.team|lane[HNW][0-9]|camera.ready|\bEDAS\b|KANBAN|PROJECT_PLAN|blind.rank|venue.rank" "$CTRL" | wc -l)
if [ "$c_hits" -lt 3 ]; then
  echo "[G0 FAIL] sweep went blind: only $c_hits/3 control files fired"; exit 1
fi
echo "[G0 ok] calibration control fired on $c_hits/3 planted files"

# --- G1: internal-vocabulary sweep ---------------------------------------------
# HARD patterns must be zero. EVIDENCE-tolerated patterns are frozen run
# metadata inside result logs (machine-local paths recorded by the pipeline
# when the run happened; rewriting logs would falsify evidence) or staging
# defaults the reproduction path needs.
HARD='zesty_coffee_herring|clumsy_pink_chimpanzee|/home/alitonia|red.team|lane[HNW][0-9]|\bEDAS\b|KANBAN|PROJECT_PLAN|blind.rank|venue.rank|camera.ready'
EVIDENCE='/mnt/data|/workspace/rag_eval|hunopapa|round-[0-9]'
echo "[G1] internal-vocabulary sweep over $BUNDLE"
h_hits=$(grep -rniE "$HARD" "$BUNDLE" || true)
if [ -n "$h_hits" ]; then
  echo "[G1 FAIL] hard-gate hits (adjudicate each):"
  sed -n '1,25p' <<<"$h_hits"
  fail=1
else
  echo "[G1 ok] zero hard-gate hits"
fi
s_hits=$(grep -rniE "$EVIDENCE" "$BUNDLE" || true)
if [ -n "$s_hits" ]; then
  echo "[G1 note] evidence-tolerated hits (frozen log fields / staging defaults), per file:"
  sed -n '1,200p' <<<"$s_hits" | cut -d: -f1 | sort | uniq -c | sort -rn
else
  echo "[G1 note] zero evidence-tolerated hits"
fi

# --- G2: exclusion check ---------------------------------------------------------
echo "[G2] exclusion check"
excl_fail=0
for p in reports docs notebooks pod_artifacts Draft.docx instrument_candidates \
         kappa_grading KAPPA_INSTRUCTIONS questions_in_progress sample_gold \
         create_github_issues build_blind_packs make_regrag_vn_release; do
  if find "$BUNDLE" -iname "*$p*" | grep -q .; then
    echo "[G2 FAIL] shipped tree contains: $p"
    find "$BUNDLE" -iname "*$p*" | head -3
    excl_fail=1
  fi
done
if [ "$excl_fail" -eq 0 ]; then
  echo "[G2 ok] no internal dirs or one-off artifacts in the shipped tree"
fi
fail=$((fail + excl_fail))

# --- G3: replay gate --------------------------------------------------------------
echo "[G3] replay: recompute Tables I/II from the shipped log with the shipped scorer"
"$PY" "$BUNDLE/scripts/compute_tables.py" --out "$REPLAY/replay_tables.json" >/dev/null
"$PY" - "$REPLAY/replay_tables.json" "$BUNDLE/data/eval/tables_paper_2026-11-16-goldfix.json" <<'EOF'
import json, sys
def load(p):
    d = json.load(open(p))
    d.pop("generated_utc", None)
    d.get("campaign_provenance", {}).pop("generated_at", None)
    return d
a, b = load(sys.argv[1]), load(sys.argv[2])
keys = ["table1_by_model_mode", "table2_by_mode_pooled", "tier1_rag_arm_identical_answers"]
diff = [k for k in keys if a.get(k) != b.get(k)]
if diff:
    print("[G3 FAIL] replay diverges from shipped tables:", diff)
    sys.exit(1)
print("[G3 ok] replay reproduces Tables I/II and the arm-equivalence count exactly")
EOF

# --- G4: integrity -----------------------------------------------------------------
echo "[G4] sha256 integrity"
SHA_ABS="$(cd "$(dirname "$SHAFILE")" && pwd)/$(basename "$SHAFILE")"
n_hashes=$(wc -l < "$SHAFILE")
if ( cd "$BUNDLE" && sha256sum -c --quiet "$SHA_ABS" ); then
  echo "[G4 ok] all $n_hashes hashes match"
else
  echo "[G4 FAIL] hash mismatch"
  fail=1
fi

if [ "$fail" -ne 0 ]; then
  echo "[AUDIT FAILED] adjudicate the failing gates above"; exit 1
fi
echo "[AUDIT PASSED] $BUNDLE"
