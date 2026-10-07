#!/usr/bin/env python3
"""Candidate instrument selector for Tier-2 v2 (RegRAG-VN sequel).

Scans the landed tmquan/thuvienphapluat-vn-vbpl shards, filters to the
money-and-banking legal area and our instrument classes (Thong tu, Nghi dinh,
Thong tu lien tich, Van ban hop nhat), excludes instruments already in
data/raw_legal/DOC_MANIFEST.json, ranks by substance (num_articles), and emits
a ranked candidate list for the ~70-instrument Tier-2 v2 build.

The output is a CANDIDATE list for human/author review, not a build decision.

Run:  .venv/bin/python scripts/select_banking_instruments.py
Out:  reports/instrument_candidates_2026-10-08.md + data/eval/instrument_candidates_v2.csv
"""

from __future__ import annotations

import csv
import glob
import json
import os
import re
import sys

import pyarrow.parquet as pq

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARD_GLOB = os.path.join(REPO_ROOT, "data", "external", "tvpl_vbpl", "documents-*.parquet")
MANIFEST = os.path.join(REPO_ROOT, "data", "raw_legal", "DOC_MANIFEST.json")
CSV_OUT = os.path.join(REPO_ROOT, "data", "eval", "instrument_candidates_v2.csv")
MD_OUT = os.path.join(REPO_ROOT, "reports", "instrument_candidates_2026-10-08.md")

DOC_TYPES = {"Thông tư", "Nghị định", "Thông tư liên tịch", "Văn bản hợp nhất"}
AREA_KEYS = ("ngan hang", "tien te")


def norm_id(raw: str) -> str:
    """Normalize a citation id like '06/2019/TT-NHNN' for dedupe."""
    s = re.sub(r"\s+", "", (raw or "")).upper()
    m = re.match(r"^(\d{1,4})/(\d{4})/(.+)$", s)
    if m:
        return f"{int(m.group(1))}/{m.group(2)}/{m.group(3)}"
    return s


def title_number(ascii_title: str):
    """Pull (number, year, kind-token) from folded titles like
    'Thong tu 39 2016 TT NHNN ...' / 'Nghi dinh 88 2023 ND CP ...'."""
    t = (ascii_title or "").lower()
    m = re.search(r"\b(thong tu|nghi dinh|thong tu lien tich|vbhn)\s+(\d{1,4})\s+(\d{4})\b", t)
    if not m:
        return None
    kind = {"thong tu": "TT", "nghi dinh": "ND", "thong tu lien tich": "TTLT", "vbhn": "VBHN"}[m.group(1)]
    return int(m.group(2)), m.group(3), kind


def main() -> int:
    with open(MANIFEST, encoding="utf-8") as f:
        man = json.load(f)
    existing = {norm_id(v) for v in man.get("urls", {}).values() if v}
    print(f"existing instruments in manifest: {len(existing)}")

    shards = sorted(glob.glob(SHARD_GLOB))
    print(f"landed shards: {len(shards)}")

    rows = []
    seen_ids = set()
    scanned = 0
    for shard in shards:
        table = pq.read_table(shard, columns=[
            "id", "doc_type", "doc_number", "year", "title", "url",
            "legal_area", "tier_name", "num_articles", "num_khoan", "status"])
        scanned += table.num_rows
        for i in range(table.num_rows):
            area = (table.column("legal_area")[i].as_py() or "")
            if not any(k in area.lower() for k in AREA_KEYS):
                continue
            dtype = table.column("doc_type")[i].as_py()
            if dtype not in DOC_TYPES:
                continue
            num = table.column("doc_number")[i].as_py()
            year = table.column("year")[i].as_py()
            title = table.column("title")[i].as_py() or ""
            num_s = num if isinstance(num, str) else ""
            # EN/VN rows of the same instrument share the number/year prefix but
            # carry different slug suffixes; key on (number/year, doc_type) so a
            # bilingual pair collapses to one candidate.
            head = re.match(r"^(\d{1,4})/(\d{4})", num_s)
            if head:
                dedup_key = f"{int(head.group(1))}/{head.group(2)}/{dtype}"
            else:
                tn = title_number(title)
                dedup_key = f"{tn}/{dtype}" if tn else f"title:{title[:60]}"
            nid = norm_id(num_s) if num_s else ""
            if nid and nid != "NONE" and nid in existing:
                continue
            if dedup_key in existing or dedup_key in seen_ids:
                continue
            seen_ids.add(dedup_key)
            rows.append({
                "doc_type": dtype,
                "number": num if isinstance(num, str) else "",
                "year": year if isinstance(year, str) else "",
                "title": title[:160],
                "url": table.column("url")[i].as_py(),
                "area": area,
                "tier": table.column("tier_name")[i].as_py(),
                "articles": int(table.column("num_articles")[i].as_py() or 0),
                "khoan": int(table.column("num_khoan")[i].as_py() or 0),
                "status": table.column("status")[i].as_py() or "",
            })

    rows.sort(key=lambda r: -r["articles"])
    os.makedirs(os.path.dirname(CSV_OUT), exist_ok=True)
    with open(CSV_OUT, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["doc_type"])
        w.writeheader()
        w.writerows(rows)

    lines = [
        "# Tier-2 v2 banking instrument candidates — 2026-10-08\n",
        f"- shards scanned: {len(shards)} ({scanned:,} docs)",
        f"- after area + doc-type filter and dedupe vs the {len(existing)} existing instruments: "
        f"**{len(rows)} candidates** (full list: `data/eval/instrument_candidates_v2.csv`)",
        "",
        "## Top 60 by substance (num_articles)\n",
        "| # | Type | Number | Year | Arts | Status | Title |",
        "|---|------|--------|------|------|--------|-------|",
    ]
    for n, r in enumerate(rows[:60], 1):
        lines.append(f"| {n} | {r['doc_type']} | {r['number']} | {r['year']} | "
                     f"{r['articles']} | {r['status'][:20]} | {r['title'][:90]} |")
    text = "\n".join(lines) + "\n"
    os.makedirs(os.path.dirname(MD_OUT), exist_ok=True)
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(text[:2500])
    print(f"\ncsv -> {CSV_OUT}\nmd  -> {MD_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
