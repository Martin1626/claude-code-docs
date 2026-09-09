import json, os, glob, collections, datetime

DIR = 'C:/Users/ai_martint/.claude/projects/c--Git-alzask'
files = sorted(glob.glob(os.path.join(DIR, '*.jsonl')), key=os.path.getsize, reverse=True)
print('sessions:', len(files), '| celkem MB:', round(sum(os.path.getsize(f) for f in files) / 1048576, 1))
print()

# 1) jake typy zaznamu vubec existuji + hledej cokoli s "compact" v klici nebo hodnote
types = collections.Counter()
compact_hits = collections.Counter()
compact_examples = []
subtypes = collections.Counter()

for fp in files:
    with open(fp, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            t = o.get('type')
            types[t] += 1
            for k in o.keys():
                if 'compact' in k.lower():
                    compact_hits['key:' + k] += 1
                    if len(compact_examples) < 6:
                        compact_examples.append((os.path.basename(fp), k, str(o.get(k))[:200]))
            st = o.get('subtype')
            if st:
                subtypes[str(t) + '/' + str(st)] += 1
            # isCompactSummary / compactMetadata varianty
            s = json.dumps(o, ensure_ascii=False)
            if '"isCompactSummary"' in s or 'compactMetadata' in s or 'compact_boundary' in s:
                compact_hits['payload'] += 1

print('--- typy zaznamu ---')
for k, v in types.most_common():
    print(' ', v, k)
print()
print('--- subtypy ---')
for k, v in subtypes.most_common(15):
    print(' ', v, k)
print()
print('--- vyskyty "compact" ---')
for k, v in compact_hits.most_common():
    print(' ', v, k)
print()
for fn, k, val in compact_examples:
    print('  PRIKLAD |', fn, '|', k, '=', val)
