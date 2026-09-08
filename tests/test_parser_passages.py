"""Unit tests for LegalDocumentParser using 64 gold CSV passages and synthetic edge cases."""

import os
import unittest

from regrag.corpus.canonical import (
    extract_article_id,
    fold_diacritics,
    normalize_ws,
)
from regrag.corpus.parser import LegalDocumentParser
from regrag.corpus.qa_loader import load_gold_questions
from regrag.provenance import CORPUS_TIER2


class TestParserPassages(unittest.TestCase):
    """Evaluates LegalDocumentParser against the 64 trusted CSV gold passages."""

    @classmethod
    def setUpClass(cls) -> None:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        csv_path = os.path.join(repo_root, "data", "gold", "bank_qa_data.csv")
        cls.questions = load_gold_questions(csv_path, repo_root=repo_root)

    def test_64_passages_article_segmentation(self) -> None:
        """Verify article segmentation on all 64 passages.

        63 of 64 passages segment cleanly to the expected article_id.
        Question Q007 fails because its passage is a sub-clause point citation
        ('Điểm c Khoản 1 Điều 18...') rather than a legal document article header.
        This failure is documented as an empirical finding, not masked.
        """
        self.assertEqual(len(self.questions), 64)
        failures = []

        for q in self.questions:
            expected_art = extract_article_id(q.gold_passage)
            parser = LegalDocumentParser(doc_id=q.id, doc_title="Test Document")
            chunks, report = parser.parse_with_report(q.gold_passage)

            chunk_arts = [c.article_id for c in chunks]
            if expected_art not in chunk_arts:
                failures.append(
                    {
                        "question_id": q.id,
                        "expected_art": expected_art,
                        "extracted_arts": chunk_arts,
                        "passage_snippet": q.gold_passage[:70],
                        "report": report,
                    }
                )

        # Q007 is the only genuine failure
        failed_ids = [f["question_id"] for f in failures]
        self.assertEqual(
            failed_ids,
            ["Q007"],
            f"Expected only Q007 to fail article segmentation, but got: {failed_ids}",
        )
        self.assertEqual(len(self.questions) - len(failures), 63)

    def test_passages_text_preservation(self) -> None:
        """Verify no passage that segments loses text.

        The concatenation of chunk texts must preserve 100% of the input passage content
        under canonical normalize_ws.
        """
        exact_matches = []
        folded_matches = []
        mismatches = []

        for q in self.questions:
            if q.id == "Q007":
                # Q007 does not contain an article header and is evaluated in test_64_passages_article_segmentation
                continue

            parser = LegalDocumentParser(doc_id=q.id, doc_title="Test Document")
            chunks, _report = parser.parse_with_report(q.gold_passage)

            combined_text = " ".join(c.text for c in chunks)
            norm_passage = normalize_ws(q.gold_passage)
            norm_chunks = normalize_ws(combined_text)

            if norm_passage == norm_chunks:
                exact_matches.append(q.id)
            elif fold_diacritics(norm_passage) == fold_diacritics(norm_chunks):
                folded_matches.append(q.id)
            else:
                mismatches.append((q.id, norm_passage[:50], norm_chunks[:50]))

        self.assertEqual(
            mismatches,
            [],
            f"Passages with text loss: {mismatches}",
        )
        # All 63 segmentable passages preserve text exactly under NFC normalisation
        self.assertEqual(len(exact_matches), 63)

    def test_preamble_captured(self) -> None:
        """Verify preamble text before the first Điều is captured into a chunk and report."""
        raw_text = """CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

Căn cứ Luật Các tổ chức tín dụng ngày 18 tháng 01 năm 2024;
Thống đốc Ngân hàng Nhà nước ban hành Thông tư:

Điều 1. Phạm vi điều chỉnh
1. Thông tư này quy định về dịch vụ thẻ ngân hàng.
"""
        parser = LegalDocumentParser(doc_id="18/2024/TT-NHNN", doc_title="Thông tư thẻ")
        chunks, report = parser.parse_with_report(raw_text)

        self.assertTrue(report["preamble_captured"])
        self.assertIn("Căn cứ Luật Các tổ chức tín dụng", report["preamble_text"])

        # Preamble chunk is chunk 0
        preamble_chunk = chunks[0]
        self.assertEqual(preamble_chunk.chunk_id, "18/2024/TT-NHNN_preamble")
        self.assertEqual(preamble_chunk.article_id, "0")
        self.assertEqual(preamble_chunk.article_title, "Lời nói đầu")
        self.assertIsNone(preamble_chunk.clause_id)
        self.assertTrue(preamble_chunk.metadata.get("is_preamble"))
        self.assertIn("Căn cứ Luật Các tổ chức tín dụng", preamble_chunk.text)

        # Article 1 is chunk 1
        art1_chunk = chunks[1]
        self.assertEqual(art1_chunk.article_id, "1")
        self.assertEqual(art1_chunk.clause_id, "1")

    def test_phan_and_chuong_nesting(self) -> None:
        """Verify Luật structure with Phần (Part) above Chương (Chapter)."""
        raw_text = """Phần thứ nhất. NHỮNG QUY ĐỊNH CHUNG
Chương I. PHẠM VI VÀ ĐỐI TƯỢNG
Điều 1. Phạm vi điều chỉnh
1. Luật này quy định về các tổ chức tín dụng.
Chương II. GIẢI THÍCH TỪ NGỮ
Điều 2. Giải thích từ ngữ
1. Tổ chức tín dụng là doanh nghiệp...
"""
        parser = LegalDocumentParser(doc_id="32/2024/QH15", doc_title="Luật Các TCTD")
        chunks, _report = parser.parse_with_report(raw_text)

        self.assertEqual(len(chunks), 2)
        # First chunk has nested Phần / Chương
        self.assertEqual(
            chunks[0].chapter,
            "Phần thứ nhất: NHỮNG QUY ĐỊNH CHUNG / Chương I: PHẠM VI VÀ ĐỐI TƯỢNG",
        )
        self.assertEqual(
            chunks[0].metadata.get("part"), "Phần thứ nhất: NHỮNG QUY ĐỊNH CHUNG"
        )
        self.assertEqual(
            chunks[0].metadata.get("chapter"), "Chương I: PHẠM VI VÀ ĐỐI TƯỢNG"
        )

        # Second chunk updates chapter under the same part
        self.assertEqual(
            chunks[1].chapter,
            "Phần thứ nhất: NHỮNG QUY ĐỊNH CHUNG / Chương II: GIẢI THÍCH TỪ NGỮ",
        )

    def test_pdf_artefacts(self) -> None:
        """Verify robustness against OCR/PDF extraction defects."""
        # 1. Split diacritics: "Đi ều 8", "Điều8", title on following line
        raw_text = """Đi ều 8
Chuyển tiền thực hiện hoạt động chuẩn bị đầu tư
1. Trước khi được cấp phép.
Điều9. Nguyên tắc vay vốn
Trang 15 / 50
Tổ chức tín dụng thực hiện cho vay đúng quy định.
"""
        parser = LegalDocumentParser(doc_id="TEST_DOC", doc_title="Test Title")
        chunks, report = parser.parse_with_report(raw_text)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0].article_id, "8")
        self.assertEqual(
            chunks[0].article_title, "Chuyển tiền thực hiện hoạt động chuẩn bị đầu tư"
        )
        self.assertEqual(chunks[0].clause_id, "1")

        self.assertEqual(chunks[1].article_id, "9")
        self.assertEqual(chunks[1].article_title, "Nguyên tắc vay vốn")

        # Stray footer "Trang 15 / 50" was filtered into dropped_lines
        self.assertGreaterEqual(report["lines_dropped"], 1)
        self.assertIn("Trang 15 / 50", report["dropped_lines"])
        self.assertNotIn("Trang 15 / 50", chunks[1].text)

    def test_document_with_no_dieu(self) -> None:
        """Verify document with no Điều returns empty list and loud report warnings."""
        raw_text = """CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc

Văn bản hướng dẫn nội bộ về nghiệp vụ giao dịch ngân quỹ.
Không chứa quy định viện dẫn điều luật.
"""
        parser = LegalDocumentParser(doc_id="INTERNAL_DOC", doc_title="Internal Guide")
        chunks, report = parser.parse_with_report(raw_text)

        self.assertEqual(chunks, [])
        self.assertEqual(report["articles_found"], 0)
        self.assertFalse(report["preamble_captured"])
        self.assertGreater(report["lines_dropped"], 0)
        self.assertTrue(
            any("No articles" in w for w in report["warnings"]),
            f"Expected warning about no articles, got: {report['warnings']}",
        )

    def test_corpus_source_stamping(self) -> None:
        """Verify corpus_source defaults to CORPUS_TIER2 and can be overridden."""
        sample_doc = """Điều 1. Phạm vi
1. Quy định về thẻ.
"""
        # Default stamps CORPUS_TIER2
        parser_default = LegalDocumentParser(doc_id="DOC1", doc_title="Doc 1")
        chunks_default = parser_default.parse(sample_doc)
        self.assertEqual(chunks_default[0].corpus_source, CORPUS_TIER2)

        # Overridden via init
        parser_custom = LegalDocumentParser(
            doc_id="DOC2", doc_title="Doc 2", corpus_source="custom_fixture"
        )
        chunks_custom = parser_custom.parse(sample_doc)
        self.assertEqual(chunks_custom[0].corpus_source, "custom_fixture")

        # Overridden via parse parameter
        chunks_override = parser_default.parse(sample_doc, corpus_source="adhoc_source")
        self.assertEqual(chunks_override[0].corpus_source, "adhoc_source")


if __name__ == "__main__":
    unittest.main()
