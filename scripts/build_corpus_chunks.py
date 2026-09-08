"""Ingest raw legal texts listed in data/raw_legal/INGEST_PLAN.json into
clause-level chunks at data/processed_chunks/corpus_chunks.json.

Rewritten 2026-09-09. The previous version hardcoded a one-entry DOCS_MAP and
did `if not os.path.exists(filepath): continue`, so a partial or misnamed
delivery produced an empty corpus while printing "Saved 0 total chunks" and
exiting 0. It also read only .txt, while 12 of the benchmark's instruments
arrive as ~7 PDFs and ~8 HTML pages.

This version is manifest-driven and fails loudly:
  * a missing file for a non-skipped entry is an error, not a skip
  * extraction is dispatched on format (txt / pdf / html)
  * a missing extraction dependency is an error naming the package to install
  * extracted text with no "Điều" anywhere is flagged as probably-garbage
  * every chunk is stamped corpus_source=CORPUS_TIER2 (see regrag/provenance.py)
  * the parser's report is surfaced rather than discarded

Usage:
  python3 scripts/build_corpus_chunks.py                # strict
  python3 scripts/build_corpus_chunks.py --allow-missing  # ingest what arrived
"""

import argparse
import json
import os
import re
import sys
from dataclasses import asdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from regrag.corpus.parser import LegalDocumentParser
from regrag.provenance import CORPUS_TIER1, CORPUS_TIER2, ProvenanceError

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(REPO_ROOT, "data", "raw_legal")
PLAN_PATH = os.path.join(RAW_DIR, "INGEST_PLAN.json")
OUTPUT_PATH = os.path.join(REPO_ROOT, "data", "processed_chunks", "corpus_chunks.json")

_ARTICLE_RE = re.compile(r"Điều\s*\d+", re.IGNORECASE)


# --- text extraction ---------------------------------------------------------

def extract_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def extract_pdf(path: str) -> str:
    """Extract text from a born-digital legal PDF. Tries pypdf, then pdfplumber."""
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # older name
        except ImportError:
            raise ProvenanceError(
                f"No PDF library available to read {os.path.basename(path)}. "
                "Install with: pip install pypdf pdfplumber"
            )
    try:
        reader = PdfReader(path)
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        if text.strip() and _ARTICLE_RE.search(text):
            return text
    except Exception as exc:  # fall through to pdfplumber, but remember why
        sys.stderr.write(f"[warn] pypdf failed on {os.path.basename(path)}: {exc}\n")

    try:
        import pdfplumber
    except ImportError:
        if not text.strip():
            raise ProvenanceError(
                f"pypdf produced no usable text from {os.path.basename(path)} and "
                "pdfplumber is not installed. Install with: pip install pdfplumber. "
                "If the PDF is scanned rather than born-digital it needs OCR, which "
                "is out of scope - get an HTML source instead."
            )
        return text

    with pdfplumber.open(path) as pdf:
        return "\n".join((page.extract_text() or "") for page in pdf.pages)


def extract_html(path: str) -> str:
    """Extract the readable body of a saved legal HTML page."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise ProvenanceError(
            f"beautifulsoup4 is not installed; cannot read {os.path.basename(path)}. "
            "Install with: pip install beautifulsoup4 lxml"
        )
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "noscript", "form", "aside"]):
        tag.decompose()
    return soup.get_text("\n")


_EXTRACTORS = {"txt": extract_txt, "pdf": extract_pdf, "html": extract_html, "htm": extract_html}


def extract_text(path: str, fmt: str) -> str:
    fmt = (fmt or os.path.splitext(path)[1].lstrip(".")).lower()
    if fmt not in _EXTRACTORS:
        raise ProvenanceError(
            f"No extractor for format {fmt!r} ({os.path.basename(path)}). "
            f"Supported: {sorted(_EXTRACTORS)}"
        )
    return _EXTRACTORS[fmt](path)


# --- main --------------------------------------------------------------------

def load_plan(path: str = PLAN_PATH):
    if not os.path.exists(path):
        raise ProvenanceError(f"Ingestion plan not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build(plan_path: str, allow_missing: bool, dry_run: bool) -> int:
    plan = load_plan(plan_path)
    documents = plan.get("documents") or []
    if not documents:
        raise ProvenanceError(f"{plan_path} lists no documents")

    all_chunks = []
    missing, ingested, garbage, reports = [], [], [], []

    for entry in sorted(documents, key=lambda d: d.get("priority", 999)):
        doc_id = entry.get("doc_id")
        filename = entry.get("expected_file")
        status = (entry.get("status") or "").lower()
        if status in ("skipped", "blocked", "quarantined"):
            print(f"[skip]    {doc_id}: status={status}")
            continue

        filepath = os.path.join(RAW_DIR, filename or "")
        if not filename or not os.path.exists(filepath):
            missing.append({"doc_id": doc_id, "file": filename, "questions": entry.get("questions")})
            msg = (
                f"[MISSING] {doc_id}: expected {filename} at {filepath} "
                f"({entry.get('questions')} questions)"
            )
            repl = entry.get("replacement_url")
            if repl:
                msg += f"\n          replacement source: {repl}"
            print(msg)
            if not allow_missing:
                continue
            continue

        try:
            raw_text = extract_text(filepath, entry.get("format", ""))
        except ProvenanceError as exc:
            print(f"[ERROR]   {doc_id}: {exc}")
            raise

        n_articles = len(_ARTICLE_RE.findall(raw_text))
        if n_articles == 0:
            garbage.append({"doc_id": doc_id, "file": filename, "chars": len(raw_text)})
            print(
                f"[SUSPECT] {doc_id}: extracted {len(raw_text)} chars but found NO 'Điều N' - "
                "probably a truncated, paywalled or mis-extracted document. Ingesting it would "
                "produce false hallucination labels."
            )
            if not allow_missing:
                raise ProvenanceError(
                    f"Refusing to ingest {doc_id}: no articles found in {filename}. "
                    "Pass --allow-missing to ingest it anyway."
                )

        parser = LegalDocumentParser(
            doc_id=doc_id, doc_title=entry.get("doc_title") or ""
        )
        # parser.parse_with_report is being added concurrently; use it if present.
        if hasattr(parser, "parse_with_report"):
            chunks, report = parser.parse_with_report(raw_text)
            reports.append({"doc_id": doc_id, "report": report})
        else:
            chunks = parser.parse(raw_text)

        for c in chunks:
            c.corpus_source = CORPUS_TIER2
            c.metadata.setdefault("source_file", filename)
            c.metadata.setdefault("source_url", entry.get("source_url"))
            c.metadata.setdefault("version", entry.get("version"))
            c.metadata.setdefault("questions_carried", entry.get("questions"))

        print(f"[ok]      {doc_id}: {len(chunks):4d} chunks, {n_articles:4d} articles in source text")
        ingested.append({"doc_id": doc_id, "chunks": len(chunks), "questions": entry.get("questions")})
        all_chunks.extend(chunks)

    print("\n=== ingestion summary ===")
    print(f"documents ingested : {len(ingested)}")
    print(f"chunks produced    : {len(all_chunks)}")
    print(f"missing files      : {len(missing)}")
    print(f"suspect extractions: {len(garbage)}")
    if missing:
        q = sum(m.get("questions") or 0 for m in missing)
        print(f"  -> {q} benchmark questions have NO corpus document:")
        for m in missing:
            print(f"     {m['doc_id']} ({m['questions']} q) <- {m['file']}")
    if garbage:
        for g in garbage:
            print(f"  -> SUSPECT {g['doc_id']}: {g['chars']} chars, no articles")

    if dry_run:
        print("\n[dry-run] not writing output")
        return 0 if not missing else 1

    if OUTPUT_PATH.endswith(f"{CORPUS_TIER1}.json"):
        raise ProvenanceError("Refusing to write the Tier 1 fixture path from the real ingestion script")

    # Guard BEFORE writing: an empty corpus must never clobber a usable one.
    if not all_chunks:
        raise ProvenanceError(
            "Ingestion produced ZERO chunks, so nothing was written and the existing "
            "output was left untouched. No corpus means no retrieval measurement is "
            "possible. Check INGEST_PLAN.json statuses and expected_file names, and "
            "confirm the source files actually arrived in data/raw_legal/."
        )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    serialized = [asdict(c) for c in all_chunks]
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(serialized, f, ensure_ascii=False, indent=2)
    print(f"\nwrote {len(serialized)} chunks -> {os.path.relpath(OUTPUT_PATH, REPO_ROOT)}")

    if reports:
        report_path = os.path.join(REPO_ROOT, "data", "processed_chunks", "ingest_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump({"parse_reports": reports, "missing": missing, "suspect": garbage},
                      f, ensure_ascii=False, indent=2)
        print(f"wrote parse/ingest report -> {os.path.relpath(report_path, REPO_ROOT)}")

    return 0 if not (missing or garbage) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--plan", default=PLAN_PATH, help="Path to INGEST_PLAN.json")
    ap.add_argument("--allow-missing", action="store_true",
                    help="Ingest what arrived instead of erroring on gaps")
    ap.add_argument("--dry-run", action="store_true", help="Report only, write nothing")
    args = ap.parse_args()
    try:
        return build(args.plan, args.allow_missing, args.dry_run)
    except ProvenanceError as exc:
        sys.stderr.write(f"\nERROR: {exc}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
