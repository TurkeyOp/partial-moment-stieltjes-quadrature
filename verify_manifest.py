#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, sys
ROOT=Path(__file__).resolve().parent
manifest=ROOT/'SHA256_MANIFEST.csv'
fail=[]
with manifest.open(newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        p=ROOT/row['path']
        if not p.is_file(): fail.append((row['path'],'missing')); continue
        if p.stat().st_size!=int(row['size_bytes']): fail.append((row['path'],'size')); continue
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        if h!=row['sha256']: fail.append((row['path'],'sha256'))
print(f'Verified {sum(1 for _ in csv.DictReader(manifest.open(encoding="utf-8")))} manifest entries; failures={len(fail)}')
for item in fail[:20]: print(item)
raise SystemExit(1 if fail else 0)
