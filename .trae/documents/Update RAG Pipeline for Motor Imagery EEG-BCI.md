## Objectives
- Narrow scope to Motor Imagery (MI) EEG-BCI classification papers
- Search only Google Scholar, PubMed, IEEE Xplore; optionally enrich DOIs via CrossRef
- Re-run pipeline with updated parameters and refresh PRISMA metrics
- Produce a minimal paper list with `name`, `author`, `source` columns
- Clean unused files and refactor for clarity

## Scope & Query Updates
- Restrict sources in `run_pipeline.py` to PubMed, IEEE Xplore, Google Scholar (src/run_pipeline.py:33–63)
- Update `config.yaml` queries to target MI-specific terms:
  - PubMed: `(("motor imagery"[Title/Abstract] OR MI[Title/Abstract] OR "imagined movement"[Title/Abstract]) AND ("electroencephalography"[MeSH Terms] OR EEG OR "brain computer interface") AND ("deep learning" OR "neural network" OR CNN OR LSTM OR transformer OR classifier OR classification)) AND (2019[Date - Publication] : 2024[Date - Publication])`
  - IEEE: `(motor imagery OR MI OR "imagined movement" OR "left hand" OR "right hand" OR foot OR tongue) AND (EEG OR electroencephalography OR "brain-computer interface" OR BCI) AND ("deep learning" OR "neural network" OR CNN OR RNN OR LSTM OR transformer) AND (classification OR accuracy OR f1)`
  - Google Scholar: `"motor imagery" EEG BCI classification (CNN OR LSTM OR transformer OR "deep learning") 2019..2024`
- Keep CrossRef (`connectors/crossref_connector.py`) as optional DOI enrichment only, not a primary source

## Screening Criteria Changes
- Title/Abstract Screener (src/screeners/title_abstract_screener.py:6–8, 19–63):
  - Add MI keywords: `['motor imagery','mi','imagined movement','left hand','right hand','foot','tongue','bci competition']`
  - Require presence of at least one MI keyword in title/abstract in addition to EEG and classification terms
  - Preserve date and language checks
- Full-Text Screener (src/screeners/full_text_screener.py:4–36):
  - Add MI keyword check to `DL_KEYWORDS` gate (or a parallel MI gate) and validate metrics

## Connectors & Retrieval
- PubMed (`connectors/pubmed_connector.py:15`): reuse, feed updated query
- IEEE Xplore (`connectors/ieee_connector.py:10`): reuse, feed updated query; ensure API key present
- Google Scholar (`connectors/scholar_connector.py:8`): reuse with user-agent and throttling, pages configurable
- Optional: After retrieval, use CrossRef to enrich missing DOI/title normalization (`connectors/crossref_connector.py:7`)

## Deduplication & Storage
- Continue DOI and fuzzy-title dedupe (src/utils/dedupe.py:30–98)
- Normalize final records to minimal schema for the requested list: `name` (title), `author` (authors joined), `source`
- Produce two CSVs via exporters:
  - Full CSV (existing): `artifacts/records_deduped.csv` (src/exporters/csv_exporter.py:4–34)
  - Minimal CSV (new): `artifacts/records_minimal.csv` with columns `name, author, source`

## Orchestration Changes
- `run_pipeline.py`:
  - Remove CrossRef and repository harvesting from primary flow; keep CrossRef optional enrichment after initial record merge
  - Recompute counts and write PRISMA JSON (src/exporters/json_exporter.py used via `write_prisma_json` in src/run_pipeline.py:79–114)
  - Add call to new minimal CSV exporter after dedupe and screening

## PRISMA Update
- Refresh `artifacts/prisma_counts.json` using updated source counts and dedupe outputs (src/run_pipeline.py:79–114)
- Regenerate Mermaid PRISMA diagram in `artifacts/prisma_diagram.md` from new counts (update Identification/Screening/Eligibility/Included values)

## Cleanup & Refactor
- Remove or archive unused connectors: `connectors/repo_connector.py` and any unused artifacts in `artifacts/search_results/`
- Ensure `.env.example` documents required keys: `PUBMED_API_KEY`, `IEEE_API_KEY`, `GEMINI_API_KEY`
- Harmonize record fields across connectors (`id,title,authors,year,doi,abstract,url,source`)

## Validation
- Dry run: execute with `--dry-run` to verify retrieval, dedupe size, and screening distributions
- Full run: execute without `--dry-run` to fetch full texts where possible and finalize exports
- Spot-check top MI results across sources for correctness

## Deliverables
- Updated `config.yaml` with MI queries
- Updated `run_pipeline.py` to restrict sources and add minimal CSV export
- Updated screeners for MI focus
- `artifacts/records_deduped.csv` and `artifacts/records_minimal.csv`
- Updated `artifacts/prisma_counts.json` and `artifacts/prisma_diagram.md`

## Assumptions
- IEEE and PubMed API keys are available
- Google Scholar scraping is allowed within rate limits
- Date range remains 2019–2024 (can extend to 2025 on request)

## Next Step
- On approval, I will implement the above changes, run a dry run to validate counts and MI focus, then perform the full run to update PRISMA and artifacts.