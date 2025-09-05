# Prompt Specifications

This folder contains the tutoring prompts used to elicit **non-revealing, Socratic hints** from code-capable LLMs.  
Prompts are written for two learner profiles — **beginner** and **advanced** — and are aligned with the Non-Revealing Feedback Policy.

## Files
- `policy_non_revealing.txt` — ground rules the model must obey.
- `system_prompt_beginner.txt` — supportive, step-by-step guidance.
- `system_prompt_advanced.txt` — concise, technical guidance.
- `few_shots.md` — three labeled exemplars (typo, conceptual, reasoning).
- `template_inference.txt` — single template with placeholders for runtime.
- `prompt_checklist.md` — QC checklist used before running evaluations.

## Output Contract (used by evaluation)
Every model response must follow this schema:

