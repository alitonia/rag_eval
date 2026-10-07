# External dataset audit — 2026-10-08

## Provenance (data/external_provenance.json)

- `zalo2021`: huggingface.co/datasets/GreenNode/zalo-ai-legal-text-retrieval-vn | license: MIT (mirror card) | trust: TRUSTED
  - Mirror packaging is MIT; upstream platform terms may still restrict redistribution of thuvienphapluat-derived text. Full dump has 3,298 qrels (MTEB card understates).
- `alqac2024`: huggingface.co/datasets/huyhuy123/ViLQA | license: research purposes only; commercial use requires author contact | trust: RESEARCH-ONLY
  - Free-text answers; article gold absent from dump (harvest via citation extractor, then human-verify).
- `alqac2025`: huggingface.co/datasets/VietTung04/alqac_2025 (ungated mirror) | license: NONE on mirror | trust: UNTRUSTED
  - Do not train or release derivatives until the canonical license is verified or access to nguyenlab/ALQAC is granted.
- `tvpl_vbpl`: huggingface.co/datasets/tmquan/thuvienphapluat-vn-vbpl | license: CC-BY-4.0 (mirror card) | trust: TRUSTED
  - 121-shard structured corpus (~738k docs): doc_type/tier/legal_area/citations pre-parsed. Spot-verify a sample against official vbpl.vn before releasing any derivative.
- `tvpl_hdpl`: huggingface.co/datasets/tmquan/thuvienphapluat-vn-hdpl | license: other (read card before any release) | trust: RESEARCH-ONLY
  - Consultation Q&A; user questions are real-citizen text - paraphrase before publishing anything.
- `tvpl_tnpl`: huggingface.co/datasets/tmquan/thuvienphapluat-vn-tnpl | license: other (read card before any release) | trust: RESEARCH-ONLY
- `hoidap_200k`: huggingface.co/datasets/phuocsang/hoidap-thuvienphapluat-200k | license: MIT (dataset card) | trust: TRUSTED
  - ~200k consultation Q&A pairs; same upstream-platform caveat as zalo2021.
- `legal_claim_verification`: huggingface.co/datasets/FinnPham52/vietnamese-legal-claim-verification | license: NONE | trust: UNTRUSTED
  - evidence_passages + verifier train/val. Verify authorship/paper before any use beyond internal reading.
- `vibidlqa`: huggingface.co/datasets/ntphuc149/ViBidLQA_v1 (repo github.com/ntphuc149/ViLQA, MIT) | license: Apache-2.0 (dataset card) | trust: TRUSTED
  - MRC format (question/context/answer); 3,013 rows.
- `vlegal_bench`: github.com/hieunguyen1053/vlegal-bench (git clone, depth 1) | license: CC BY-NC-ND 4.0 (DATASET LICENSE AGREEMENT) | trust: RESEARCH-ONLY
  - ND clause: evaluate + cite only; NO derivatives, NO merging into our released bundle, NO redistribution under our name. 22 MCQ tasks, 23 jsonl, 77 MB.
- (not downloaded) vlqa_canonical: arXiv 2507.19995 dataset - UNRELEASED (paper says 'coming soon'); email authors for access
- (not downloaded) alqac_canonical_gated: huggingface.co/datasets/nguyenlab/ALQAC - requires access approval
- (not downloaded) court_portals: ansvn/congbobanan/anle.toaan.gov.vn - DNS-blocked from this machine; user browser fetch
- (not downloaded) news_corpora: jasong03/vov_phapluat, jasong03/nhandan_phapluat, myduy/vnexpress_plain_text_phap_luat - open but NO license stated; UNTRUSTED until provenance checked

## Files on disk

- `zalo2021/.gitattributes` (2,561 bytes)
- `zalo2021/README.md` (7,896 bytes)
- `zalo2021/corpus.jsonl` (114,990,275 bytes)
- `zalo2021/queries.jsonl` (552,125 bytes)
- `zalo2021/corpus/test-00000-of-00001.parquet` (33,647,874 bytes)
- `zalo2021/qrels/test-00000-of-00001.parquet` (33,551 bytes)
- `zalo2021/qrels/test.jsonl` (73,068 bytes)
- `zalo2021/qrels/train.jsonl` (231,094 bytes)
- `zalo2021/queries/test-00000-of-00001.parquet` (68,428 bytes)
- `alqac2024/.gitattributes` (2,461 bytes)
- `alqac2024/README.md` (2,848 bytes)
- `alqac2024/readme.md` (2,531 bytes)
- `alqac2024/data/train-00000-of-00001.parquet` (19,993,070 bytes)
- `vibidlqa/.gitattributes` (2,419 bytes)
- `vibidlqa/README.md` (5,139 bytes)
- `vibidlqa/ViBidLQA_test.jsonl` (831,135 bytes)
- `vibidlqa/ViBidLQA_train.jsonl` (2,763,989 bytes)
- `vibidlqa/ViBidLQA_val.jsonl` (672,433 bytes)
## Zalo 2021 (GreenNode mirror, MIT per card)

- corpus.jsonl: 61425 docs, fields ['_id', 'text', 'title']
- text chars: min 0, median 829, max 252881
- queries.jsonl: 3298 queries
- qrels train+test: 3298 (fields ['corpus-id', 'query-id', 'score'])
- harvest on 500 sampled corpus docs: 500/500 yield a (document, article) pair via regrag citation extraction
- example doc (_id=01/2009/tt-bnn+1): title='Điều 1. Phạm vi áp dụng' text_head='Thông tư này hướng dẫn tuần tra, canh gác bảo vệ đê Điều trong mùa lũ đối với các tuyến đê sông được phân loại, phân cấp'

## ALQAC 2024 dump (huyhuy123/ViLQA, research-only per card)

- parquet: /mnt/data/seminar_2/data/external/alqac2024/data/train-00000-of-00001.parquet, rows: 43588
- fields: ['Answer', 'ID', 'ID1', 'Question', 'idx']
- citation harvest over ALL 43588 answers: 36716 (84%) carry any citation, 36716 (84%) name an instrument, 36716 (84%) yield a (instrument, article) pair = candidate gold pending human verification
  - e.g. Q='Thực hiện cắt giảm hồ sơ thay đổi mức vốn điều lệ của ngân hàng hợp tác xã trong quý 2 năm' -> 32/2024/QH15 / Điều 200
  - e.g. Q='Thỏa thuận cho vay giữa khách hàng và ngân hàng có phải lập thành văn bản không?' -> 39/2016/TT-NHNN / Điều 23
  - e.g. Q='Khách hàng có thể vay ngân hàng theo hình thức nào?' -> 39/2016/TT-NHNN / Điều 10

## ViBidLQA (ntphuc149, Apache-2.0 per card)

- .gitattributes (2419 bytes)
- README.md (5139 bytes)
- ViBidLQA_test.jsonl (831135 bytes)
- ViBidLQA_train.jsonl (2763989 bytes)
- ViBidLQA_val.jsonl (672433 bytes)
- ViBidLQA_test.jsonl: 603 rows, fields ['answer', 'context', 'question']
  sample: {"context": "Luật Đấu thầu số 22/2023/QH15 Điều 35. Phương thức lựa chọn nhà đầu tư khoản 3 . Phương thức hai giai đoạn một túi hồ sơ: Phương thức hai giai đoạn một túi hồ sơ đ
- ViBidLQA_train.jsonl: 1928 rows, fields ['answer', 'context', 'question']
  sample: {"context": "Luật Đấu thầu số 22/2023/QH15 Điều 55. Lựa chọn nhà thầu cung cấp thuốc, hóa chất, vật tư xét nghiệm, thiết bị y tế khoản 3 . Trường hợp các cơ sở khám bệnh, ch
- ViBidLQA_val.jsonl: 482 rows, fields ['answer', 'context', 'question']
  sample: {"context": "Nghị định hướng dẫn Luật Đấu thầu số 22 Điều 21. Công khai thông tin về lựa chọn nhà thầu khoản 1 . Các thông tin về lựa chọn nhà thầu được đăng tải công khai trê

## thuvienphapluat structured corpus (tmquan vbpl mirror, CC-BY-4.0)

- shards read: 95, documents: 567,851
- docs with real Vietnamese text (>200 chars): 566,904
- total parsed articles: 1,811,573, clauses (Khoản): 4,214,619
- document types (top 12): [('Quyết định', 261997), ('Công văn', 124169), ('Nghị quyết', 43918), ('Kế hoạch', 34228), ('Thông tư', 24487), (None, 22519), ('Thông báo', 16082), ('Chỉ thị', 15337), ('Nghị định', 9379), ('Văn bản hợp nhất', 4595), ('Thông tư liên tịch', 2381), ('Hướng dẫn', 2112)]
- tiers: [('provincial & administrative', 307240), ('official letters & standards', 143253), ('central decisions & directives', 67656), ('primary legislation', 49702)]
- legal areas (top 12): [('Bo may hanh chinh', 135000), ('Thue Phi Le Phi', 46524), ('Thuong mai', 35245), ('Tai chinh nha nuoc', 33229), ('Xuat nhap khau', 33018), ('Bat dong san', 29626), ('Doanh nghiep', 25277), ('Van hoa Xa hoi', 22154), ('Dau tu', 22042), ('Xay dung Do thi', 21523), ('Lao dong Tien luong', 20824), ('Tai nguyen Moi truong', 19263)]
- docs in banking/finance-adjacent legal areas: 41,180 [('Tai chinh nha nuoc', 33229), ('Tien te Ngan hang', 7951)]

## Consultation dump: tvpl_hdpl

- not downloaded yet

## Consultation dump: hoidap_200k

- not downloaded yet

## Consultation dump: tvpl_tnpl

- not downloaded yet

## Contamination check vs our 88 benchmark questions

- our questions exactly contained in ALQAC dump: 0/88
- our questions exactly contained in Zalo queries: 0/88
- exact-match containment only; near-duplicates are NOT covered by this check, so any future training use of these dumps still needs an embedding-level dedup pass
