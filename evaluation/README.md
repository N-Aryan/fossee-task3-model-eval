# Evaluation — Quick Start

This folder contains the **end-to-end evaluation scaffold** for FOSSEE Task 3.

## Workflow
1. **Generate model outputs** for each buggy snippet:
   ```bash
   python evaluation/evaluate.py --model codet5 --level beginner
   ```
This reads ```examples/labels.csv```, builds a prompt using ```prompts/```, and writes:
1. Raw outputs → results/raw/<model>/<filename>.txt
2. Log CSV → results/predictions_<model>.csv (filename, gold_label, model_output)

**Score discrimination (automatic):**
```bash
python evaluation/compute_metrics.py --pred results/predictions_codet5.csv
```
Produces confusion matrix + per-class precision/recall/F1 →
```results/metrics_codet5.json``` and prints a table.

**Score hint quality (human):**
1. Open evaluation/hint_scores_template.csv
2. Fill 0–3 for each dimension:
     1. Clarity
     2. Non-Revealing
     3. Actionability
     4. Learner-Fit
3. Save as results/hint_scores_<model>.csv
(Optional) Add overall column = sum of 4 criteria (0–12)

**Output Contract (model)**

Each response must contain:
```
Diagnosis: <typo|conceptual|reasoning|uncertain>
Hint: <one or two sentences, no corrected code>
```
Reproducibility Notes
1. Student level: --level beginner|advanced
2. Few-shots: append from prompts/few_shots.md if needed
3. Keep temperature low (e.g., 0.2) for deterministic outputs
4. Document run notes for transparency

