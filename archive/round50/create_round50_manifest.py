#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib
ROOT=Path(__file__).resolve().parent
rows=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.name=='SHA256_MANIFEST.csv' or any(part in {'__pycache__'} for part in p.parts):
        continue
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    rows.append({'path':str(p.relative_to(ROOT)),'size_bytes':p.stat().st_size,'sha256':h})
with (ROOT/'SHA256_MANIFEST.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['path','size_bytes','sha256']);w.writeheader();w.writerows(rows)
print(f'Wrote {len(rows)} checksums')
