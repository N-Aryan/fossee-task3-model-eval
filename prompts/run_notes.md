# Run Notes (Reproducibility)

- **Levels**: beginner (default) | advanced (flag: `--level advanced`)  
- **Few-shots**: disabled by default, enable with `--fewshots`  
- **Sampling parameters** (recommended for evaluation):  
  - temperature = 0.2  
  - top_p = 0.9  
  - max_new_tokens ≈ 200  

- **Output contract**:
```
Diagnosis: <typo|conceptual|reasoning|uncertain>
Hint: <one or two sentences, no corrected code>
```

- **Logging**:  
  - Raw outputs → `evaluation/results/raw/<model>/<filename>.txt`  
  - Predictions CSV → `evaluation/results/predictions_<model>.csv`
