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

---

### ✅ Step 2: `docs/Research_Report.md` polish
- Top par ek **Table of Contents** daalo (anchors).
- End mein ek **Acknowledgment** line add karo:
  > This scaffold was developed as part of FOSSEE Autumn 2025 task submission.

---

### ✅ Step 3: Root-level README.md mein ek **Final polish**
- Already tumne TL;DR aur quick links daal diye.
- Ab ek aur **badge-style polish** daal sakte ho top pe:
  - License badge
  - Python version badge
  - HuggingFace models badge (optional, fake bhi chalega demo ke liye).

Example:
```markdown
![MIT License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
