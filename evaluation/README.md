# Evaluation Results

This folder stores **model outputs and scoring artifacts**.

## Contents
- **raw/** → Raw text outputs from models (Diagnosis + Hint per snippet).  
- **predictions_<model>.csv** → Structured logs with filename, gold_label, predicted_label, and hint.  
- **metrics_<model>.json** → Auto-computed confusion matrix and F1 scores.  
- **hint_scores_<model>.csv** → Human rubric scoring (Clarity, Non-Revealing, Actionability, Learner-Fit).

## Notes
- All outputs follow the **contract**:
```
Diagnosis: <typo|conceptual|reasoning|uncertain>
Hint: <one or two sentences, no corrected code>
```
- The files here include **demo runs** for illustration.  
They are meant to show expected format, not actual benchmarks.  

For detailed workflow, see [`evaluation/README.md`](../README.md).
