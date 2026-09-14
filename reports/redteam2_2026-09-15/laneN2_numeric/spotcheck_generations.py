#!/usr/bin/env python3
"""Read-only spot-check of generations.json for laneN2 numeric re-audit."""
import json, collections

P = '/mnt/data/seminar_2/data/eval/generations.json'
rows = json.load(open(P))

print('== totals ==')
print('rows:', len(rows))
print('models:', dict(collections.Counter(r.get('model_name') for r in rows)))
print('modes:', dict(collections.Counter(r.get('retrieval_mode') for r in rows)))
print('distinct questions:', len(set(r.get('question_id') for r in rows)))
print('finish_reason:', dict(collections.Counter(r.get('finish_reason') for r in rows)))
print('row keys:', sorted(rows[0].keys()))

for k in ('seed', 'temperature', 'max_new_tokens', 'quantization', 'quant_config', 'gpu', 'gpu_name', 'prompt_hash'):
    vals = collections.Counter(str(r.get(k)) for r in rows)
    print(f'{k}:', dict(list(vals.items())[:5]))

# how are probes flagged?
probe_flag = [k for k in rows[0].keys() if 'probe' in k.lower() or 'answerable' in k.lower()]
print('probe-ish keys:', probe_flag)

def probe_rows(r):
    for k in ('is_probe', 'probe', 'unanswerable'):
        if k in r:
            return bool(r[k])
    if 'answerable' in r:
        return not r['answerable']
    # fallback: gold_citation null heuristics
    return None

SENT_EXACT = 'THÔNG TIN KHÔNG CÓ TRONG TÀI LIỆU'

def has_sent(a):
    return SENT_EXACT.lower() in (a or '').lower()

cb = [r for r in rows if r.get('retrieval_mode') == 'closed_book']
print('\n== closed-book ==')
print('cb rows:', len(cb))
hedges = [r for r in cb if has_sent(r.get('raw_response')) and len((r.get('raw_response') or '').strip()) > len(SENT_EXACT) + 30]
print('cb sentinel-then-substance (approx, +30 chars):', len(hedges))
probes_cb = [r for r in cb if probe_rows(r) is True]
ans_cb = [r for r in probes_cb if not has_sent(r.get('raw_response'))]
print('cb probe rows:', len(probes_cb), 'answered (no sentinel):', len(ans_cb))

vis = [r for r in rows if r.get('model_name') == 'vistral-7b' and probe_rows(r) is True]
vis_ref = [r for r in vis if has_sent(r.get('raw_response'))]
print('vistral probe rows:', len(vis), 'with sentinel:', len(vis_ref))

# alternative probe identification: gold_citation None
if probe_rows(rows[0]) is None:
    def is_probe2(r):
        g = r.get('gold_citation')
        return g is None or g in (None, {}, [], 'null')
    probes_cb2 = [r for r in cb if is_probe2(r)]
    print('cb probe rows (gold_citation null):', len(probes_cb2),
          'answered:', sum(1 for r in probes_cb2 if not has_sent(r.get('raw_response'))))

print('\n== example rows ==')
for qid, mode, model in (('Q006', 'closed_book', 'qwen-7b'),
                         ('Q008', 'closed_book', 'qwen-7b'),
                         ('Q059', 'rag_bm25', None)):
    cands = [r for r in rows if r.get('question_id') == qid
             and r.get('retrieval_mode') == mode
             and (model is None or r.get('model_name') == model)]
    print(f'--- {qid} {mode} model={model}: {len(cands)} row(s)')
    for r in cands[:3]:
        a = (r.get('raw_response') or '').replace('\n', ' | ')
        print('   model:', r.get('model_name'), '| finish:', r.get('finish_reason'))
        print('   answer head:', a[:400])
        if qid == 'Q059':
            print('   contains 61/2025:', '61/2025' in (r.get('raw_response') or ''),
                  '| contains Dieu 3:', ('Điều 3' in (r.get('raw_response') or '')) or ('Điều 3 ' in (r.get('raw_response') or '')))
