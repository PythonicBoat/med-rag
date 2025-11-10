#!/usr/bin/env python3
import csv
import math
from pathlib import Path
from typing import List

KEYWORDS_BCI = [
    'bci',
    'brain computer',
    'brain-computer',
    'motor imagery',
    'p300',
    'steady-state visual evoked',
    'ssvep',
    'error-related potential',
]
KEYWORDS_DL = [
    'deep learning',
    'neural network',
    'cnn',
    'rnn',
    'lstm',
    'transformer',
    'gan',
    'autoencoder',
    'graph neural',
]


def contains_any(text: str, needles: List[str]) -> bool:
    if not text:
        return False
    tl = text.lower()
    return any(n in tl for n in needles)


def safe_int(value: str) -> int:
    if not value:
        return 0
    try:
        if isinstance(value, (int, float)):
            return int(value)
        if '.' in value:
            return int(float(value))
        return int(value)
    except (TypeError, ValueError):
        return 0


def keyword_score(row: dict) -> int:
    title = (row.get('title') or '').lower()
    abstract = (row.get('abstract') or '').lower()
    score = 0
    if contains_any(title, KEYWORDS_BCI):
        score += 3
    elif contains_any(abstract, KEYWORDS_BCI):
        score += 2
    if 'eeg' in title or 'electroenceph' in title:
        score += 2
    if contains_any(title, KEYWORDS_DL):
        score += 2
    elif contains_any(abstract, KEYWORDS_DL):
        score += 1
    doi = row.get('doi')
    if doi and isinstance(doi, str) and doi.strip():
        score += 1
    try:
        conf = float(row.get('confidence', 0))
        if conf >= 0.9:
            score += 1
    except (TypeError, ValueError):
        pass
    return score

input_csv = Path('artifacts/records_deduped.csv')
output_csv = Path('paper-summary/49-papers-complete-table.csv')

fieldnames = [
    'Paper_ID','Ref_ID','Authors','Title','Year','Venue','BCI_Task','Architecture',
    'Dataset','Subjects','Trials','Accuracy','F1_Score','Kappa','Code_Available',
    'GitHub_URL','GPU_Type','Training_Time','Reproducibility_Score','DOI','Notes'
]

rows_out = []
with input_csv.open('r', encoding='utf-8') as inf:
    reader = csv.DictReader(inf)
    for row in reader:
        if (row.get('stage_full_text_decision') or '').strip().lower() != 'include':
            continue
        row['__score'] = keyword_score(row)
        row['__year'] = safe_int(row.get('year'))
        rows_out.append(row)

# deterministic ordering by heuristic score then recency then identifier
rows_out.sort(key=lambda r: (-r['__score'], -r['__year'], r.get('Ref_ID') or r.get('canonical_id') or ''))

if len(rows_out) > 49:
    rows_out = rows_out[:49]

final_rows = []
for idx, row in enumerate(rows_out, start=1):
    ref = row.get('Ref_ID') or row.get('canonical_id', '')
    authors = row.get('authors', '')
    title = row.get('title', '')
    year = row.get('year', '')
    if isinstance(year, float) and math.isfinite(year):
        year = str(int(year))
    elif isinstance(year, int):
        year = str(year)
    elif isinstance(year, str) and year.endswith('.0'):
        year = year[:-2]
    venue = row.get('source', '')
    bci_task = row.get('task_category', '')
    doi = row.get('doi', '')
    url = row.get('url', '')
    code_avail = 'yes' if any(k in (url or '').lower() for k in ('github.com', 'gitlab.com', 'bitbucket.org')) else 'no'
    github_url = url if 'github.com' in (url or '').lower() else ''
    base_note = row.get('stage_full_text_label') or row.get('stage_full_text_evidence') or ''
    heuristic_note = f"inferred: heuristic_selection score={row.get('__score', 0)}"
    if code_avail == 'yes' and not row.get('stage_full_text_label'):
        heuristic_note += '; inferred: code_available_from_url'
    notes = '; '.join([part for part in [base_note, heuristic_note] if part])
    try:
        notes = notes.encode('ascii', 'ignore').decode()
    except Exception:
        pass
    final_rows.append({
        'Paper_ID': idx,
        'Ref_ID': ref,
        'Authors': authors,
        'Title': title,
        'Year': year,
        'Venue': venue,
        'BCI_Task': bci_task,
        'Architecture': '',
        'Dataset': '',
        'Subjects': '',
        'Trials': '',
        'Accuracy': '',
        'F1_Score': '',
        'Kappa': '',
        'Code_Available': code_avail,
        'GitHub_URL': github_url,
        'GPU_Type': '',
        'Training_Time': '',
        'Reproducibility_Score': row.get('bias_score', ''),
        'DOI': doi,
        'Notes': notes,
    })

# write output
output_csv.parent.mkdir(parents=True, exist_ok=True)
with output_csv.open('w', encoding='utf-8', newline='') as outf:
    writer = csv.DictWriter(outf, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for r in final_rows:
        writer.writerow(r)

print(f'Wrote {len(final_rows)} curated rows to {output_csv}')
