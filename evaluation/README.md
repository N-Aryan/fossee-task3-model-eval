# Evaluation — Quick Start

This folder contains the **end-to-end evaluation scaffold** for FOSSEE Task 3.

---

## Workflow

### 1. Generate model outputs
Run the evaluation script for each buggy snippet:

```bash
python evaluation/evaluate.py --model codet5 --level beginner
```
This will:

- Read examples/labels.csv
- Build prompts from prompts/
- Write outputs:
  1. Raw → evaluation/results/raw/<model>/<filename>.txt
  2. Log CSV → evaluation/results/predictions_<model>.csv



### 2. Score discrimination (automatic)
Compute per-class metrics:
```
python evaluation/compute_metrics.py --pred evaluation/results/predictions_codet5.csv
```
Outputs:
- Confusion matrix
- Precision / Recall / F1
- JSON dump → evaluation/results/metrics_codet5.json

### 3. Score hint quality (human)
1. Open evaluation/hint_scores_template.csv
2. Fill 0–3 for each dimension:
 - Clarity
 - Non-Revealing
 - Actionability
 - Learner-Fit
3. Save as evaluation/results/hint_scores_<model>.csv
(Optional) Add an overall column = sum of 4 criteria (0–12).


### Output Contract (model)
Each model response must strictly follow:
```
Diagnosis: <typo | conceptual | reasoning | uncertain>
Hint: <one or two sentences, no corrected code>
```
### Reproducibility Notes

- Student level: --level beginner | advanced
- Few-shots: append from prompts/few_shots.md if needed
- Sampling: keep temperature low (e.g. 0.2) for deterministic outputs
- Always log run notes in prompts/run_notes.md for transparency
