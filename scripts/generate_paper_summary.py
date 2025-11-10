#!/usr/bin/env python3
import csv
from pathlib import Path

input_csv = Path('artifacts/records_deduped.csv')
output_csv = Path('paper-summary/49-papers-complete-table.csv')

fieldnames = [
    'Paper_ID','Ref_ID','Authors','Title','Year','Venue','BCI_Task','Architecture',
    'Dataset','Subjects','Trials','Accuracy','F1_Score','Kappa','Code_Available',
    'GitHub_URL','GPU_Type','Training_Time','Reproducibility_Score','DOI','Notes'
]

rows_out = []
with input_csv.open('r', encoding='utf-8') as inf:
    # read using csv with liberal quoting
    reader = csv.DictReader(inf)
    pid = 1
    for row in reader:
        ta = row.get('stage_title_abstract_decision','').strip()
        ft = row.get('stage_full_text_decision','').strip()
        # select records that passed title/abstract screening
        if ta.lower() == 'include':
            ref = row.get('canonical_id','')
            authors = row.get('authors','')
            title = row.get('title','')
            year = row.get('year','')
            # remove trailing .0 from year if present
            if year.endswith('.0'):
                year = year[:-2]
            venue = row.get('source','')
            bci_task = row.get('task_category','')
            doi = row.get('doi','')
            url = row.get('url','')
            code_avail = 'yes' if ('github.com' in (url or '') or row.get('source','').lower()=='repositories') else 'no'
            github_url = url if 'github.com' in (url or '') else ''
            notes = row.get('stage_full_text_label','') or row.get('stage_full_text_evidence','') or ''
            rows_out.append({
                'Paper_ID': pid,
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
                'Reproducibility_Score': row.get('bias_score',''),
                'DOI': doi,
                'Notes': notes,
            })
            pid += 1

# write output
output_csv.parent.mkdir(parents=True, exist_ok=True)
with output_csv.open('w', encoding='utf-8', newline='') as outf:
    writer = csv.DictWriter(outf, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for r in rows_out:
        writer.writerow(r)

print(f'Wrote {len(rows_out)} candidate rows to {output_csv}')
