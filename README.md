# Evaluating Open-Source Models for Student Competence Analysis (Python)

> FOSSEE Autumn 2025 — Python Screening Task 3  
> Author: Aryan Narang

## Executive Summary
- **Objective.** Move beyond error detection to analyze **student competence**—discriminating **typo**, **conceptual**, and **reasoning** mistakes—and produce **non-revealing, Socratic hints**.
- **Models considered.** CodeT5 (encoder–decoder), CodeBERT (encoder baseline), StarCoder (decoder-only LLM).
- **Evaluation axes.**  
  1) **Mistake-type discrimination:** confusion matrix and per-class F1.  
  2) **Hint quality:** Clarity, Non-Revealing, Actionability, Learner-Fit (0–3 each; total /12).
- **Repository contents.** Labeled buggy snippets, prompt specifications (beginner/advanced), scoring rubric, and results templates.
- **Why open-source.** Reproducible and deployable in educational settings without vendor lock-in.

## Quick Links
- **Full paper-style write-up:** [`docs/DEEP_README.md`](docs/DEEP_README.md)  
- **Examples (dataset):** [`examples/`](examples/) • [`labels.csv`](examples/labels.csv)  
- **Prompt specifications:** [`prompts/`](prompts/) (beginner, advanced, few-shots)  
- **Evaluation scaffold:** [`evaluation/`](evaluation/) (`evaluate.py`, `scoring.md`)  
- **References:** [`references.md`](references.md) • License: MIT

## How to Review (Rapid)
1. Scan the **Results templates** below.  
2. Open 1–2 files in `examples/` and the corresponding model outputs/notes.  
3. Verify rubric dimensions in `evaluation/scoring.md` (especially **Non-Revealing** policy).  
4. For full context, read [`docs/DEEP_README.md`](docs/DEEP_README.md).

## Conceptual Pipeline
Student code → Model analysis → **Classify** (typo / conceptual / reasoning) → **Generate** a Socratic hint (no solution) → Student revises.

<details>
<summary><b>Model survey (compact)</b></summary>

- **CodeBERT** (encoder, ~125M, MIT): efficient representations; suitable for classification baselines; **not generative** (no hints natively).  
- **CodeT5** (encoder–decoder, ~220M/770M, Apache-2.0): understands + generates; controllable; typically concise, non-revealing hints; sometimes terse.  
- **StarCoder** (decoder-only, 15.5B, OpenRAIL-M): strongest analysis and fluent hints; risk of “over-helping” (solution leakage) without strict prompting; higher compute.

</details>

## Evaluation Rubrics (Summary)
- **Mistake-type discrimination:** confusion matrix + per-class F1 for {typo, conceptual, reasoning}.  
- **Hint quality (0–3 each; /12 total):**  
  - **Clarity** — understandable phrasing.  
  - **Non-Revealing** — avoids giving the solution.  
  - **Actionability** — directs the next step.  
  - **Learner-Fit** — appropriate for the assumed level.

See full descriptors in [`evaluation/scoring.md`](evaluation/scoring.md).

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

> **Policy.** Hints must **not** include full corrected code. Prefer questions and micro-diagnostics.

## Repository Structure
