#!/usr/bin/env python3
import csv
from pathlib import Path

infile = Path('paper-summary/49-papers-complete-table.csv')
outfile = Path('reproducibility/code-availability-assessment.csv')

with infile.open('r', encoding='utf-8') as inf:
    reader = csv.DictReader(inf)
    rows = [r for r in reader if r.get('Code_Available','').strip().lower() == 'yes']

outfile.parent.mkdir(parents=True, exist_ok=True)
with outfile.open('w', encoding='utf-8', newline='') as outf:
    writer = csv.DictWriter(outf, fieldnames=['Paper_ID','Ref_ID','Code_Available','GitHub_URL','Notes'])
    writer.writeheader()
    for r in rows:
        writer.writerow({'Paper_ID': r.get('Paper_ID',''), 'Ref_ID': r.get('Ref_ID',''), 'Code_Available': r.get('Code_Available',''), 'GitHub_URL': r.get('GitHub_URL',''), 'Notes': r.get('Notes','')})

print(f'Wrote {len(rows)} code-availability rows to {outfile}')
