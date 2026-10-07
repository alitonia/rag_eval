# External dataset audit — 2026-10-08

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
- example doc (cid=None): title='Điều 1. Phạm vi áp dụng' text_head='Thông tư này hướng dẫn tuần tra, canh gác bảo vệ đê Điều trong mùa lũ đối với các tuyến đê sông được phân loại, phân cấp'

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

## Contamination check vs our 88 benchmark questions

- our questions exactly contained in ALQAC dump: 0/88
- our questions exactly contained in Zalo queries: 0/88
- exact-match containment only; near-duplicates are NOT covered by this check, so any future training use of these dumps still needs an embedding-level dedup pass
