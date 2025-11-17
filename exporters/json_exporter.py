import json
import os


def write_prisma_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_prisma_mermaid(counts: dict, path: str):
    records_by_source = counts.get('records_by_source') or counts.get('records_identified') or {}
    allowed_sources = {'PubMed', 'IEEE Xplore', 'Google Scholar'}
    records_by_source = {k: v for k, v in records_by_source.items() if k in allowed_sources}
    total_identified = counts.get('total_identified') or sum(records_by_source.values())
    de_dup = counts.get('de_dup_count') or 0
    screened = de_dup
    excluded_ta = counts.get('excluded_title_abstract') or 0
    fulltext_assessed = counts.get('fulltext_assessed') or 0
    ft_excluded_detail = counts.get('fulltext_excluded_detail') or {}
    included = counts.get('included') or 0

    lines = [
        '# PRISMA 2020 Flow Diagram',
        '',
        '```mermaid',
        'flowchart TB',
        '    id1["Identification of studies via databases"]',
        '    id2["Records identified from:',
    ]
    # source breakdown
    src_lines = []
    src_lines.append(f'    Databases (n = {total_identified})')
    for src, n in records_by_source.items():
        src_lines.append(f'    • {src} (n = {n})')
    lines.append('\n'.join(src_lines) + '"]')
    # screening and eligibility
    lines += [
        f'    id3["Records after duplicates removed\n(n = {de_dup})"]',
        f'    id4["Records screened\n(n = {screened})"]',
        f'    id5["Records excluded\n(n = {excluded_ta})"]',
        f'    id6["Full-text articles assessed \nfor eligibility\n(n = {fulltext_assessed})"]',
    ]
    # full-text excluded breakdown
    ft_total_excl = sum(ft_excluded_detail.values()) if ft_excluded_detail else 0
    ft_lines = [
        f'    id7["Full-text articles excluded (n = {ft_total_excl}):',
    ]
    for label, n in ft_excluded_detail.items():
        ft_lines.append(f'    • {label} (n = {n})')
    lines.append('\n'.join(ft_lines) + '"]')
    lines.append(f'    id8["Studies included in review\n(n = {included})"]')
    # connections
    lines += [
        '    id1 --> id2',
        '    id2 --> id3',
        '    id3 --> id4',
        '    id4 --> id5',
        '    id4 --> id6',
        '    id6 --> id7',
        '    id6 --> id8',
        '```'
    ]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
