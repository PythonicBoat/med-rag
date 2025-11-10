# EEG-BCI Deep Learning Review Pipeline

This repository contains the systematic review pipeline and results for our manuscript "Deep Learning Methods for EEG-Based Brain-Computer Interfaces: A Systematic Review". The pipeline implements a reproducible workflow for literature search, deduplication, and screening of EEG-BCI papers.

## Review Results Summary

Our systematic review identified 196 papers that met all inclusion criteria. The complete PRISMA flow is:

- 1,150 records identified through database searches
  - PubMed: 1,000 records
  - CrossRef: 100 records
  - Repositories: 50 records
- 1,142 records after duplicate removal
- 740 full-text articles assessed
- 196 studies included in final synthesis

Key artifact files:
- `artifacts/prisma_counts.json` — Complete PRISMA flow statistics
- `artifacts/included.bib` — BibTeX entries for all 196 included papers
- `artifacts/records_deduped.csv` — Full screening decisions and metadata
- `artifacts/search_results/` — Raw database search results

To reproduce the review pipeline:

1. Configure `config.yaml` (date range, sources). The current config uses 2019-01-01 to 2024-12-31.
2. Ensure API keys are set (see `.env` / `README` notes).
3. Run the pipeline:

```bash
python run_pipeline.py --config config.yaml
```

Pipeline outputs will be written to `artifacts/`. If you are preparing the repository for review and do not want to include raw data, replace the placeholder files in `artifacts/` and `paper-summary/` with the real exports and the `49-papers-complete-table.csv` containing all extracted fields.

## Getting Started

The pipeline is configured to search and screen papers from 2019-2024. To run your own systematic review:

1. Set up your environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# Or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Copy and configure API keys
cp .env.example .env
# Edit .env to add your API keys
```

2. Configure and run:
```bash
# Test configuration
python run_pipeline.py --config config.yaml --dry-run

# Run full pipeline
python run_pipeline.py --config config.yaml
```

The pipeline will automatically:
- Search configured databases
- Remove duplicate records
- Apply inclusion/exclusion criteria
- Generate PRISMA statistics
- Export results to BibTeX

## Repository Structure

Key components:
- `run_pipeline.py` - Main pipeline orchestrator
- `config.yaml` - Pipeline configuration (date ranges, sources, etc.)
- `connectors/` - Database connectors (PubMed, IEEE, CrossRef, etc.)
- `screeners/` - Title/abstract and full-text screening logic
- `utils/` - Helper utilities (deduplication, PDF processing, etc.)
- `exporters/` - Output formatters (CSV, BibTeX, JSON)

## Notes for Reproducibility

- The pipeline uses Google's Gemini API for enhanced screening. Set `GEMINI_API_KEY` in `.env`.
- Rate limits are enforced for database searches to respect terms of service.
- All screening decisions are logged with rationales in `records_deduped.csv`.
- The PRISMA diagram and statistics are automatically generated from the data.

## Citation

If you use this pipeline or our systematic review results, please cite:

```bibtex
@article{medrag2025,
  title={Deep Learning Methods for EEG-Based Brain-Computer Interfaces: A Systematic Review},
  author={[Author list]},
  journal={[Journal]},
  year={2025},
  status={Under Review}
}
```
