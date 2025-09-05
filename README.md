# Evaluating Open-Source Models for Student Competence Analysis (Python)

> FOSSEE Autumn 2025 — Python Screening Task 3  
> Author: Aryan Narang

## TL;DR (60-second overview)
- **Goal:** Debugging se aage jaakar **student competence** (typo vs conceptual vs reasoning) ko identify karna aur **non-revealing, Socratic hints** dena.
- **Models:** CodeT5 (gen), CodeBERT (encoder baseline), StarCoder (large gen).
- **How we evaluate:**  
  1) **Discrimination:** Typo vs Conceptual vs Reasoning (confusion matrix, per-class F1)  
  2) **Hint Quality:** Clarity, Non-Revealing, Actionability, Learner-Fit (0–3 each; /12)
- **What’s inside:** Labeled buggy snippets, prompt specs (beginner/advanced), scoring rubric, results templates.
- **Why open-source:** Reproducible, deployable in education without vendor lock-in.

## Quick Links
- **Deep paper-style write-up:** [`docs/DEEP_README.md`](docs/DEEP_README.md)
- **Examples (dataset):** [`examples/`](examples/) • [`labels.csv`](examples/labels.csv)
- **Prompt specs:** [`prompts/`](prompts/) (beginner, advanced, few-shots)
- **Evaluation scaffold:** [`evaluation/`](evaluation/) (`evaluate.py`, `scoring.md`)
- **References:** [`references.md`](references.md) • License: MIT

## How to Review in 3 Minutes
1. **Skim** the Results templates (below).  
2. **Open** 1–2 files in `examples/` + corresponding hints (your model runs/notes).  
3. **Check** rubric dimensions in `scoring.md` (non-revealing policy honored?).  
4. **Deep dive** if needed: [`docs/DEEP_README.md`](docs/DEEP_README.md).

## Methods in One Picture (mental model)
Student code → (Model) → *detects* typo/concept/reasoning → *generates* a **Socratic hint** (no solution) → student iterates.

<details>
<summary><b>Model survey (compact)</b></summary>

- **CodeBERT (encoder, ~125M, MIT):** Fast representations; great for classification baselines; not generative → no hints by itself.
- **CodeT5 (enc-dec, ~220M/770M, Apache-2.0):** Understands + generates; controllable; good for short, non-revealing hints; sometimes terse.
- **StarCoder (decoder-only, 15.5B, OpenRAIL-M):** Strongest analysis & fluent hints; risk of “overhelping” (solution leak) without strict prompts; heavy compute.
</details>

## Evaluation Rubrics (summary)
- **Discrimination:** confusion matrix + F1 for {typo, conceptual, reasoning}
- **Hint Quality (/12):** Clarity (0–3), Non-Revealing (0–3), Actionability (0–3), Learner-Fit (0–3)

See full descriptions in [`evaluation/scoring.md`](evaluation/scoring.md).

## Results Templates 

**Table 1 — Mistake-type discrimination**

| Model     | Typo F1 | Conceptual F1 | Reasoning F1 | Overall Acc. |
|-----------|:------:|:-------------:|:------------:|:------------:|
| CodeBERT  |        |               |              |              |
| CodeT5    |        |               |              |              |
| StarCoder |        |               |              |              |

**Table 2 — Hint quality (avg per criterion; 0–3)**

| Model     | Clarity | Non-Revealing | Actionability | Learner-Fit | **Overall /12** |
|-----------|:-------:|:-------------:|:-------------:|:-----------:|:---------------:|
| CodeT5    |         |               |               |             |                 |
| StarCoder |         |               |               |             |                 |

> Policy: **Never** include full corrected code in hints. Prefer questions + micro-diagnostics.

## Repo Layout
