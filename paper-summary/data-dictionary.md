# Data Dictionary

This document explains each column in `49-papers-complete-table.csv`.

- Paper_ID: Internal numeric ID (1..49)
- Ref_ID: Citation string (e.g., "Smith et al., 2020")
- Authors: Full author list
- Title: Paper title
- Year: Publication year
- Venue: Conference or journal name
- BCI_Task: Task performed (e.g., motor imagery, P300)
- Architecture: Deep learning model used (e.g., CNN, RNN, Transformer)
- Dataset: Name of dataset (if public)
- Subjects: Number of subjects
- Trials: Number of trials/epochs
- Accuracy: Reported accuracy (as reported by paper)
- F1_Score: Reported F1 (if provided)
- Kappa: Cohen's kappa (if provided)
- Code_Available: yes/no
- GitHub_URL: URL to code repository (if applicable)
- GPU_Type: GPU used for training (if reported)
- Training_Time: Training time reported (e.g., hours)
- Reproducibility_Score: Manual score (0-5) assessing reproducibility
- DOI: Paper DOI
- Notes: Any additional notes or exclusions
