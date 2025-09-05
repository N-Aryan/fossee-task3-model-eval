# Hint Quality Rubric (0–3 each; total /12)

**Clarity**
- 0: Hard to understand / ambiguous.
- 1: Understandable but awkward or vague.
- 2: Clear phrasing with minor rough edges.
- 3: Very clear, specific, and focused.

**Non-Revealing**
- 0: Gives the solution or code patch.
- 1: Strongly leading; near-solution.
- 2: Helpful guidance without explicit fix.
- 3: Socratic: questions / micro-diagnostics; no code disclosed.

**Actionability**
- 0: No next step implied.
- 1: Vague next step (“check your code”).
- 2: Concrete direction (e.g., “recheck loop bounds”).
- 3: Precise & scoped (“what remainder indicates even numbers?”).

**Learner-Fit**
- 0: Inappropriate tone/jargon for audience.
- 1: Occasionally mismatched.
- 2: Generally appropriate.
- 3: Well-matched to the stated level (beginner/advanced).

**Mistake-Type Discrimination**
- Scored automatically via confusion matrix comparing the parsed `Diagnosis` with `examples/labels.csv`.
