"""Tests for the per-question citation-override table.

Covers the Q059-Q061 gold fix: an override may pin a primary instrument that
URL resolution already produced (reordering candidates and rebuilding the
citation triple), must refuse to invent an instrument, and must be a no-op
for every other row. Evidence: data/gold/TT61_TRIPLE_FINDINGS.md.
"""

import os
import tempfile
import unittest

from regrag.corpus.qa_loader import (
    _apply_citation_override,
    load_citation_overrides,
    load_gold_questions,
)

CSV_HEADER = "ID,doc_link,question,answer,text_contains_answer_in_the_doc,author\n"

# Passage mirrors the Q059 gold passage shape: an article header, no instrument
# number anywhere in the passage, and a cross-reference "khoản 9" that the
# passage-header regex used to pick up as the gold clause.
AMBIGUOUS_ROW = (
    "59,https://portal.example/32law.pdf https://files.example/61-nhnn.pdf,"
    "Hoi gi do ve mang luoi?,Tra loi theo Khoan 3 Dieu 3 Thong tu 61/2025.,"
    "Điều 3. Giải thích từ ngữ \\n Trong Thông tư này: \\n "
    "1. Mạng lưới hoạt động... \\n 2. Chi nhánh... \\n "
    "3. Phòng giao dịch không được phê duyệt khoản vay vượt 02 tỷ đồng... \\n "
    "9. Khu vực nội thành... \\n "
    "10. ... không thuộc phạm vi quy định tại khoản 9 Điều này.,"
    "Hương\n"
)

MANIFEST = {
    "https://portal.example/32law.pdf": "32/2024/QH15",
    "https://files.example/61-nhnn.pdf": "61/2025/TT-NHNN",
}

OVERRIDES = {
    "Q059": {
        "primary_doc_id": "61/2025/TT-NHNN",
        "article_id": "3",
        "clause_id": "3",
        "reason": "reference answer cites Khoản 3 Điều 3 Thông tư 61/2025/TT-NHNN",
    }
}


class TestCitationOverrides(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ovr-")
        os.makedirs(os.path.join(self.tmp, "data", "gold"), exist_ok=True)
        self.csv_path = os.path.join(self.tmp, "bank_qa_data.csv")
        with open(self.csv_path, "w", encoding="utf-8") as f:
            f.write(CSV_HEADER + AMBIGUOUS_ROW)

    def _load(self, overrides):
        return load_gold_questions(
            self.csv_path, manifest=dict(MANIFEST), repo_root=self.tmp,
            overrides=overrides,
        )[0]

    def test_override_pins_primary_and_rebuilds_citation(self):
        base = self._load(None)
        self.assertEqual(base.gold_doc_ids, ["32/2024/QH15", "61/2025/TT-NHNN"])
        self.assertEqual(base.gold_citations[0]["doc_id"], "32/2024/QH15")
        self.assertEqual(base.gold_citations[0]["clause_id"], "9")

        fixed = self._load(dict(OVERRIDES))
        self.assertEqual(fixed.gold_doc_ids, ["61/2025/TT-NHNN", "32/2024/QH15"])
        cit = fixed.gold_citations[0]
        self.assertEqual(cit["doc_id"], "61/2025/TT-NHNN")
        self.assertEqual(cit["article_id"], "3")
        self.assertEqual(cit["clause_id"], "3")
        self.assertEqual(cit["confidence"], "reference-verified")
        # Row-level confidence still describes the URL situation honestly.
        self.assertEqual(fixed.doc_id_confidence, "ambiguous-multi-url")
        # The secondary candidate is retained, never dropped.
        self.assertIn("32/2024/QH15", fixed.gold_doc_ids)

    def test_override_refuses_to_invent_an_instrument(self):
        bad = {"Q059": {"primary_doc_id": "99/2099/TT-NHNN",
                        "article_id": "3", "clause_id": "3"}}
        with self.assertRaises(ValueError):
            self._load(bad)

    def test_missing_override_file_is_a_noop(self):
        other_tmp = tempfile.mkdtemp(prefix="ovr-empty-")
        qs = load_gold_questions(
            self.csv_path, manifest=dict(MANIFEST), repo_root=other_tmp
        )
        self.assertEqual(qs[0].gold_doc_ids, ["32/2024/QH15", "61/2025/TT-NHNN"])
        self.assertEqual(qs[0].gold_citations[0]["confidence"], "passage-header")

    def test_load_citation_overrides_skips_comment_keys(self):
        path = os.path.join(self.tmp, "data", "gold", "citation_overrides.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"_about": "doc", "Q059": {"article_id": "3"}}')
        table = load_citation_overrides(path)
        self.assertEqual(set(table), {"Q059"})

    def test_apply_reorders_only_existing_candidates(self):
        doc_ids, citation, conf = _apply_citation_override(
            "Q059", ["32/2024/QH15", "61/2025/TT-NHNN"], "ambiguous-multi-url",
            {"primary_doc_id": "61/2025/TT-NHNN", "article_id": "3",
             "clause_id": "3"})
        self.assertEqual(doc_ids, ["61/2025/TT-NHNN", "32/2024/QH15"])
        self.assertEqual(citation["clause_id"], "3")
        self.assertEqual(conf, "ambiguous-multi-url")


if __name__ == "__main__":
    unittest.main()
