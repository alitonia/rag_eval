#!/usr/bin/env python3
"""Systematic sweep of HuggingFace and GitHub for Vietnamese legal data sources.

Queries the keyless catalog APIs (huggingface.co/api/datasets,
api.github.com/search/repositories) over a keyword battery, then prints a
merged table: id, size/last-modified, license, and a shortened description.
Results feed docs/vn_legal_data_sources_*.md; this script is re-runnable when
a source is expected to have released since the last sweep (e.g. VLQA).

Run:  .venv/bin/python scripts/discover_hf_github_legal.py
Gentle-by-design: one request per keyword per host, ~2 s apart.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time

HF_QUERIES = [
    "vietnamese legal",
    "vietnamese law",
    "phap luat",
    "van ban phap luat",
    "thuvienphapluat",
    "zalo legal",
    "alqac",
    "vlqa",
    "vietnam statute",
    "legal corpus vi",
]
GH_QUERIES = [
    "vietnamese legal dataset",
    "thuvienphapluat",
    "vbpl crawler",
    "vietnamese law corpus",
    "alqac",
    "phap dien vietnam",
]


def curl_json(url: str):
    """curl with browser UA (urllib is sometimes reset by these hosts)."""
    out = subprocess.run(
        ["curl", "-s", "--max-time", "30", "-A",
         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36", url],
        capture_output=True, text=True, timeout=45,
    ).stdout
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def sweep_hf() -> dict:
    found = {}
    for q in HF_QUERIES:
        url = f"https://huggingface.co/api/datasets?search={q.replace(' ', '%20')}&limit=40&full=false"
        data = curl_json(url)
        time.sleep(2)
        if not isinstance(data, list):
            continue
        for d in data:
            did = d.get("id", "")
            found[did] = {
                "id": did,
                "downloads": d.get("downloads", 0) or 0,
                "likes": d.get("likes", 0) or 0,
                "modified": (d.get("lastModified") or "")[:10],
                "query": q,
            }
    return found


def sweep_gh() -> dict:
    found = {}
    for q in GH_QUERIES:
        url = f"https://api.github.com/search/repositories?q={q.replace(' ', '+')}&per_page=15"
        data = curl_json(url)
        time.sleep(3)
        if not isinstance(data, dict):
            continue
        for r in data.get("items", []) or []:
            full = r.get("full_name", "")
            found[full] = {
                "id": full,
                "stars": r.get("stargazers_count", 0) or 0,
                "size_kb": r.get("size", 0) or 0,
                "pushed": (r.get("pushed_at") or "")[:10],
                "license": (r.get("license") or {}).get("spdx_id") or "none",
                "desc": (r.get("description") or "")[:110],
                "query": q,
            }
    return found


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--only", choices=["hf", "gh"], default="both",
                    help="restrict the sweep to one catalog")
    args = ap.parse_args()

    if args.only in ("hf", "both"):
        hf = sweep_hf()
        print(f"== HuggingFace datasets ({len(hf)} unique) ==")
        for did in sorted(hf, key=lambda k: -hf[k]["downloads"]):
            h = hf[did]
            print(f"{did:<60} dl={h['downloads']:<7} likes={h['likes']:<4} mod={h['modified']} via:{h['query']}")
    if args.only in ("gh", "both"):
        gh = sweep_gh()
        print(f"\n== GitHub repositories ({len(gh)} unique) ==")
        for full in sorted(gh, key=lambda k: -gh[k]["stars"]):
            g = gh[full]
            print(f"{full:<55} stars={g['stars']:<5} {g['size_kb']:<7}KB lic={g['license']:<12} pushed={g['pushed']}")
            if g["desc"]:
                print(f"{'':<55} {g['desc']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
