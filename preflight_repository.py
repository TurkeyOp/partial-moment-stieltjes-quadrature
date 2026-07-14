from pathlib import Path
import csv, re, sys
root=Path(__file__).resolve().parent
errors=[]
required=['README.md','CITATION.cff','run_all.py','paper/jcam/main.tex','paper/jcam/main.pdf','docs/round41/novelty_defense.md','docs/round41/reference_verification.csv']
for rel in required:
    if not (root/rel).exists(): errors.append(f'missing: {rel}')
tex=(root/'paper/jcam/main.tex').read_text(encoding='utf-8')
for token in ['[Author Name]','corresponding.author@email.example','[Replace with','[Department and Institution]']:
    if token in tex: errors.append(f'placeholder remains: {token}')
with (root/'docs/round41/citation_audit.csv').open(encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['pass']!='True': errors.append(f'citation audit failed: {row["key"]}')
print('PASS' if not errors else '\n'.join(errors))
sys.exit(1 if errors else 0)
