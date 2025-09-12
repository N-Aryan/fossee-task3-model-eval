# Results (Demo)

This folder contains demo evaluation results.

- **raw/** → model raw outputs (`Diagnosis + Hint`) for buggy files.
- **predictions_demo.csv** → filename, gold label, predicted label, hint.
- **hint_scores_demo.csv** → rubric scores (clarity, non-revealing, actionability, learner-fit, total).

These are placeholder/demo runs for reproducibility illustration.  
For full evaluation:  

```bash
python evaluation/evaluate.py --model codet5 --level beginner
python evaluation/compute_metrics.py --pred evaluation/results/predictions_codet5.csv
```
> Note: The files with `_demo` suffix are only illustrative placeholders.  
> For actual evaluation, replace them with your generated results (e.g., `predictions_codet5.csv`, `hint_scores_codet5.csv`).
