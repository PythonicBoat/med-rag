# RAG EEG-BCI Pipeline

This repository contains a copy-pasteable, production-ready scaffold for a RAG-style search + dedupe + screening pipeline targeted at EEG-BCI systematic reviews.

See the top-level `run_pipeline.py` for the orchestrator and `config.yaml` for the configuration.

## Paper Artifacts

This repository accompanies the systematic review manuscript "Deep Learning Methods for EEG-Based Brain-Computer Interfaces: A Systematic Review" (under review). The following artifact folders are included to support reproducibility and reviewer access:

- `paper-summary/` — Complete table and machine-readable metadata for the 49 included papers (CSV + JSON). Fill these files with the extracted data for each included study.
- `artifacts/prisma_counts.json` — PRISMA flow data used to report screening counts (958 → 685 → 131 → 49). Provided as an example; replace with the final counts if different.
- `artifacts/search_results/` — Raw search result exports from data sources (placeholders present).
- `artifacts/excluded_papers_82.csv` — Title/abstract & full-text exclusion log with reasons for the 82 excluded records.

To reproduce the review pipeline:

1. Configure `config.yaml` (date range, sources). The current config uses 2019-01-01 to 2024-12-31.
2. Ensure API keys are set (see `.env` / `README` notes).
3. Run the pipeline:

```bash
python run_pipeline.py --config config.yaml
```

Pipeline outputs will be written to `artifacts/`. If you are preparing the repository for review and do not want to include raw data, replace the placeholder files in `artifacts/` and `paper-summary/` with the real exports and the `49-papers-complete-table.csv` containing all extracted fields.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with API keys (set GEMINI_API_KEY for Google Gemini / Generative API)
```

2. Dry-run the pipeline:

```bash
python run_pipeline.py --config config.yaml --dry-run
```

3. Run the full pipeline:

```bash
python run_pipeline.py --config config.yaml
```

Files of interest

- `connectors/` - data source connectors (PubMed, IEEE, CrossRef, Google Scholar fallback, repositories)
- `utils/` - dedupe, PDF extraction, logging utilities (includes `utils/llm.py` for Gemini integration)
- `screeners/` - title/abstract and full text screeners
- `exporters/` - CSV/JSON/BibTeX writers
- `artifacts/` - outputs and cached search logs

Notes

- Respect service TOS and rate limits when scraping (Google Scholar scraping is fragile).
- Add API keys to `.env` before running. The pipeline supports Google Gemini via the `GEMINI_API_KEY` environment variable. The `google-generativeai` client is included in `requirements.txt`.
