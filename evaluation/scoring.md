# Scoring Rubric

This file defines the criteria for evaluating model-generated hints.

---

## 1. Mistake-Type Discrimination (automatic)
- **Goal:** Does the model correctly classify the error type?
- **Labels:** `typo`, `conceptual`, `reasoning`, `uncertain`
- **Metrics:** confusion matrix, per-class Precision, Recall, F1
- **Source:** computed automatically via `compute_metrics.py`

---

## 2. Hint Quality (human, 0–3 scale)
Each hint is rated on **four dimensions**:

1. **Clarity**
   - 0 = Unclear / confusing
   - 1 = Hard to follow, vague phrasing
   - 2 = Understandable, but not polished
   - 3 = Very clear, concise, student-friendly  

2. **Non-Revealing**
   - 0 = Gives away full corrected code
   - 1 = Reveals too much, student can copy solution
   - 2 = Avoids code but gives heavy clue
   - 3 = Fully Socratic, non-revealing  

3. **Actionability**
   - 0 = No guidance, irrelevant
   - 1 = Very weak suggestion
   - 2 = Useful but incomplete
   - 3 = Directs next step clearly without solving  

4. **Learner-Fit**
   - 0 = Wrong level (too advanced / too trivial)
   - 1 = Slightly mismatched
   - 2 = Mostly suitable
   - 3 = Perfectly tailored to given level (beginner/advanced)  

---

## 3. Overall Score
- **Automatic:** F1 scores from discrimination task
- **Human:** Sum of 4 dimensions (0–12)
- **Reporting:** Stored in `evaluation/results/hint_scores_<model>.csv`

---

## Notes
- All hints must respect **Non-Revealing Policy**.
- Prefer **questions and nudges** over solutions.
- Both automatic and human scores are required for full evaluation.
