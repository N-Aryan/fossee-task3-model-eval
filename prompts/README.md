# Prompt Specifications

This folder contains the tutoring prompts used to elicit **non-revealing, Socratic hints** from code-capable LLMs.  
Prompts are written for two learner profiles — **beginner** and **advanced** — and are aligned with the Non-Revealing Feedback Policy.

## Files
- `policy_non_revealing.txt` — Ground rules the model must obey.  
- `system_prompt_beginner.txt` — Supportive, step-by-step guidance.  
- `system_prompt_advanced.txt` — Concise, technical guidance.  
- `few_shots.md` — Three labeled exemplars (typo, conceptual, reasoning) in Q–A style.  
- `template_inference.txt` — Single template with placeholders for runtime.  
- `prompt_checklist.md` — Quick checklist to verify prompts before running evaluations.

## Output Contract (used by evaluation)
Every model response must follow this schema:
```
Diagnosis: <typo | conceptual | reasoning | uncertain>
Hint: <one or two sentences, no corrected code>
```

This ensures **consistency**, **non-revealing feedback**, and **ease of scoring** across all evaluation runs.
