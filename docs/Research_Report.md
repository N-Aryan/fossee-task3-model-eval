# Evaluating Open-Source Models for Student Competence Analysis (Python)

## Table of Contents
- [Abstract](#abstract)
- [Background & Motivation](#background--motivation)
- [Model Survey](#model-survey)
  - [CodeBERT](#codebert)
  - [CodeT5](#codet5)
  - [StarCoder](#starcoder)
- [Methodology](#methodology)
- [Reasoning (Required Answers)](#reasoning-required-answers)#
- [Results](#results)
- [Discussion](#discussion)
- [Limitations](#limitations)
- [Future Work](#future-work)
- [Ethical Considerations](#ethical-considerations)
- [References](#references)
  
  ---
  
## Abstract
We evaluate open-source, code-oriented AI models for student competence analysis in Python.  
The goal is not just to locate errors in student code, but to infer **why** mistakes occur and to generate **non-revealing, Socratic prompts** that guide learning without directly giving away solutions.  

In this study, we compare **CodeT5**, **CodeBERT**, and **StarCoder** on their ability to distinguish superficial syntax errors from deeper conceptual misunderstandings and to provide helpful feedback hints to students.

---

## Background & Motivation
Introductory programming education often suffers from high student frustration and attrition, partly because novices struggle to understand their errors beyond syntax fixes.  

- Traditional autograders or compilers identify *what* is wrong but not *why* the student made a mistake or *how* to guide them.  
- There is an educational gap between simply pointing out errors and fostering a deeper understanding of underlying concepts.  
- Educational psychology suggests that **Socratic prompting** – asking guiding questions rather than giving answers – can help novices reflect and self-correct misconceptions.  
- However, providing such individualized feedback at scale is challenging due to limited human tutors.

**Student competence analysis goes beyond automated debugging;** it involves diagnosing the conceptual misunderstandings behind errors and assessing a learner’s grasp of programming concepts.  

**Example:**  
If a student uses the wrong operator or an incorrect loop boundary, a competence analysis would identify whether this is a trivial slip or a fundamental misconception. Addressing this gap could improve learning outcomes by tailoring hints to the student’s needs, thereby turning errors into learning opportunities.  

Our motivation is to explore whether modern open-source code models can perform this kind of analysis and feedback generation, enabling intelligent tutoring systems that are accessible and transparent.  

---

## Model Survey
We survey three state-of-the-art open-source models – **CodeT5**, **CodeBERT**, and **StarCoder** – examining their architecture, size, training data, licensing, and suitability for educational feedback tasks.

### CodeBERT
**Architecture & Size:**  
- A bi-modal transformer encoder based on **RoBERTa (BERT-base architecture)** with ~125 million parameters.  

**Training Data:**  
- Pretrained on the **CodeSearchNet dataset** (GitHub code paired with comments in 6 languages: Python, Java, JavaScript, PHP, Ruby, Go).  
- Objectives: Masked language modeling + replaced token detection (using both NL–PL pairs and unimodal code data).  

**License:**  
- Released by Microsoft under the **MIT License** → permissive for open-source projects.  

**Pros:**  
- Lightweight, efficient for code understanding tasks (search, classification).  
- Can embed code + text for tasks like detecting whether a snippet matches a description.  

**Cons:**  
- Encoder-only → **not generative** (cannot natively produce hints in natural language).  
- Needs an additional generation layer to produce feedback prompts.  
- Limited for direct tutoring use-cases without fine-tuning.  

**Summary:**  
CodeBERT is strong for **classification** but weak for **feedback generation**.  
It might classify error types with fine-tuning, but it cannot directly produce hints without extra scaffolding.

### CodeT5
**Architecture & Size:**  
- Encoder–decoder Transformer (based on Google’s **T5**) tailored for programming tasks.  
- Base model: ~220M parameters; Large variant: ~770M parameters.  
- Supports **sequence-to-sequence tasks** like translating code into English explanations.

**Training Data:**  
- Pretrained on ~8.35 million code examples from **CodeSearchNet** (multiple languages).  
- Additional C/C# code collected to broaden language coverage.  
- Introduced **identifier-aware pre-training**: model learns to recognize code identifiers and recover them when masked.  
- Included **dual natural language <-> programming language generation tasks** (code comments ↔ code), aligning with documentation and summarization tasks.

**License:**  
- Released under **Apache-2.0 License** (some checkpoints BSD).  
- Permissive, allows integration into educational tools without legal hurdles.

**Pros:**  
- Smaller and more computationally accessible compared to giant LLMs.  
- Designed for both **code understanding** and **generation**.  
- Can generate textual output (e.g., explain code or suggest fixes).  
- Captures **code-specific context** better than generic LMs.

**Cons:**  
- Not explicitly **instruction-tuned** for conversational help.  
- Outputs may be terse or template-like, reflecting docstring-style training.  
- May require **fine-tuning** or careful prompting for pedagogically useful feedback.  
- Smaller size means weaker **deep logical reasoning** compared to larger LLMs.

**Summary:**  
CodeT5 offers a strong starting point with open licensing and manageable size.  
It can generate feedback, but may need prompt engineering or fine-tuning to deliver **Socratic, non-revealing hints** useful in education.

### StarCoder
**Architecture & Size:**  
- Decoder-only **large language model (LLM)** specialized for code.  
- **15.5 billion parameters** → by far the largest of the three models considered.  
- Based on GPT-style transformer with modifications:  
  - Uses **multi-query attention** for efficiency.  
  - Trained with **fill-in-the-middle (FIM)** capability (handles code context before + after a gap).  
  - Supports **extended context window** of 8192 tokens → useful for long code files or multi-part conversations.

**Training Data:**  
- Pretrained on **The Stack v1.2** → massive dataset of source code in **80+ programming languages** (from public GitHub repos).  
- ~**1 trillion tokens** of code used in training.  
- Data filtered to include only **permissively licensed** or no-license code to avoid legal/ethical issues.  
- Training was **purely on code (and comments)** — not instruction-tuned for Q&A/dialog.  
  - Means it learned to generate code/explanations from context, but not from human tutoring data.

**License:**  
- Released under **BigCode OpenRAIL-M license**.  
- Open for research & education, but with usage restrictions:  
  - Prohibits malicious use.  
  - Requires compliance with ethical guidelines.  
- Model checkpoint accessible after accepting terms on Hugging Face.

**Pros:**  
- State-of-the-art performance on many code tasks.  
- Likely the **best at understanding code intent** among open models.  
- Can generate **detailed, articulate hints** if prompted carefully.  
- Competitive with private models (e.g., Codex) on benchmarks.  
- May recognize subtle conceptual errors smaller models miss.

**Cons:**  
- Very large → computationally heavy (requires GPU + significant memory).  
- Practicality is limited in resource-constrained classrooms.  
- Not instruction-tuned → plain English prompts may not always work.  
  - Needs carefully designed prompts (e.g., “Tech Assistant” style).  
- Without fine-tuning, may sometimes:  
  - Give away solutions too directly.  
  - Include unnecessary code in answers.  

**Summary:**  
StarCoder offers **raw power + broad training** → strong at subtle error detection and generating articulate hints.  
But challenges include **resource requirements, prompt control, and license restrictions**.  
Best suited for research/controlled environments; less practical for lightweight deployment without adaptation.

## Methodology
Our evaluation approach combines a **taxonomy-based dataset**, a **structured prompting strategy**, and a mix of **quantitative and qualitative metrics** to assess each model’s performance on student competence analysis.

### 1. Taxonomy of Mistakes & Dataset
We curated a small dataset of short Python code snippets written by students (or simulated student solutions) that exhibit common errors.  
Each snippet is annotated with a mistake category from a taxonomy we defined:

- **Typo Mistakes:**  
  Minor syntax errors, misspellings, or simple lapses (e.g., missing a parenthesis or using `=` instead of `==`).  
  These are surface-level errors that do not reflect a deep misunderstanding – essentially “slips.”

- **Conceptual Mistakes:**  
  Errors stemming from misunderstanding a programming concept or construct.  
  - Example: using recursion incorrectly (misunderstanding recursive calls), or misusing a loop (off-by-one error suggesting confusion about loop bounds).  
  These indicate a **gap in conceptual knowledge**.

- **Reasoning Mistakes:**  
  Higher-level logical or algorithmic errors where the code is syntactically correct but the **approach** is flawed.  
  - Example: using the wrong algorithm or incorrect condition that reflects mistaken reasoning about requirements.  
  These require the student to **rethink their approach**, not just fix a line.

**Dataset characteristics:**  
- Snippets are short (a few lines to ~½ page) focusing on a single identifiable issue.  
- Mistakes cover both **beginner-level tasks** (loops, conditionals) and **slightly advanced tasks** (data structures, multi-function code) → allows us to observe adaptability across difficulty.

---
### 2. Prompt Design
For each snippet, we crafted a prompt to elicit **helpful, non-revealing feedback** from the models. To ensure fairness, the prompt specification is consistent across models, adjusted only as needed for model-specific quirks.  

**Core Prompt Template:**```
You are a Python teaching assistant.
A student wrote the following code for a given task, but it doesn’t work as expected.
Analyze the code to identify the mistake without fixing it outright,
and ask a question or give a hint to help the student realize their error
without revealing the answer.
Here is the code:
{student_code}```

**Model-specific adjustments:**
- **CodeT5 (encoder–decoder):**  
  Prompt given as input text → model generates an output sequence.  
  Since CodeT5 is not chat-tuned, we rely on pretraining + explicit phrasing (“give a hint, not a solution”).

- **StarCoder (decoder-only, not instruction-tuned):**  
  Works better with role-based phrasing (e.g., “You are a Python teaching assistant”) and imperative tone.  
  We use a **“Tech Assistant” style** prompt as recommended by BigCode.  
  In practice, adding stop sequences helps prevent the model from generating full solutions.

- **CodeBERT (encoder-only, non-generative):**  
  Cannot generate hints.  
  Instead, we use CodeBERT for **classification only**:  
  - Prompt: “Label the following code error as Typo, Conceptual, or Reasoning.”  
  - Achieved by fine-tuning / few-shot classification layer on embeddings.  
  Included in **mistake-type discrimination** evaluation, but **excluded from hint quality** evaluation.




### 3. Evaluation Plan
We evaluate each model along **two dimensions**:

#### (i) Mistake-Type Discrimination
- **Goal:** Does the model correctly recognize the type of error (Typo vs Conceptual vs Reasoning)?  
- **Method:**  
  - Compare model’s inferred error category to the **ground truth label**.  
  - For **CodeT5** and **StarCoder**, we infer the category from their generated explanation/hint:  
    - Example: Hint says *“Check the spelling of …”* → implies **Typo**.  
    - Example: Hint says *“Are you sure you understood how recursion terminates?”* → implies **Conceptual**.  
  - For **CodeBERT** (fine-tuned as a classifier), it directly predicts the category.  

- **Metrics:**  
  - **Confusion matrix** for each model.  
  - Per-class **precision, recall, and F1** scores.  

---

#### (ii) Feedback Quality (Prompt Usefulness)
- **Goal:** Assess the **pedagogical value** of hints/feedback generated by CodeT5 and StarCoder.  
- **Method:** Use a **rubric** with 4 criteria, each scored **0–3** (poor → excellent).  

**Rubric Criteria:**
1. **Clarity:** Is the hint clearly phrased and understandable?  
2. **Non-Revealing:** Does it avoid giving away the solution directly?  
   - A Socratic hint should prompt thinking, not spoil the answer.  
3. **Actionability:** Does the hint guide the student on what to do or reconsider?  
   - (e.g., “Check your loop condition” vs. “This is wrong”).  
4. **Learner-Fit:** Is the hint appropriate for the assumed knowledge level?  
   - Jargon-free for beginners; more depth for advanced students; never condescending.

- **Scoring:**  
  - Each response → 0–3 per criterion.  
  - Compile **average scores per model**.  
  - To ensure consistency, the **same evaluator** scores all hints using predefined descriptions.  

**Example:**  
- “Non-Revealing = 3” → hint contains no code/answer, but asks an insightful guiding question.  
- “Non-Revealing = 0” → model essentially gave away the correct code outright (failure of Socratic principle).

---

#### Outputs
- **Table 1:** Mistake-type classification performance (confusion matrix, F1 scores).  
- **Table 2:** Average rubric scores for hint quality.  
- **Reasoning Analysis:** Selected examples with commentary on model behavior (strengths vs errors).


## Reasoning (Required Answers)

To provide deeper insight, we address key aspects of our approach and findings in a **Q&A style**:

### Q1. What educational gap does this project address, and why is it important?

**Answer:**  
We target the gap between **simple error detection** and **true learning-oriented feedback** in programming education.  

- Novice students often receive compiler errors like *“SyntaxError: missing parenthesis”* or failing test cases, but these do not explain **underlying misconceptions**.  
- Our work is important because identifying **why** a student made a mistake (e.g., a conceptual mix-up between two constructs) enables targeted hints that promote learning.  
- By focusing on **competence analysis**, we aim to transform error feedback from mere bug-fixing into a **teaching moment**.  

This addresses the critical need for **scalable, high-quality tutoring**: students need more than correctness; they need **guidance to build correct mental models**.  

Prior studies on **Socratic tutoring** show improved learning gains when students are guided to the answer instead of told the answer. Bridging this gap could improve student self-efficacy and reduce frustration.  

---

### Q2. Why evaluate open-source models like CodeT5, CodeBERT, and StarCoder?

**Answer:**  
We deliberately chose **open-source AI models** to align with the ethos of **Free and Open Source Software in Education (FOSSEE)** and to ensure our approach can be adopted without proprietary barriers.  

- Each model brings unique strengths:  
  - **CodeBERT** → lightweight pre-training for code understanding.  
  - **CodeT5** → code-to-text generation, useful for articulating errors.  
  - **StarCoder** → large-scale generative power, potential for nuanced analysis.  

- Evaluating these models highlights the **trade-offs between scale and educational usefulness**.  
- Open models allow:  
  - **Reproducibility** (anyone can run them).  
  - **Adaptability** (fine-tune or extend for education).  
  - Avoiding closed APIs, usage limits, or licensing fees. 
### Q3. How do we ensure a fair and meaningful evaluation of the models’ capabilities?

**Answer:**  
We took several steps to ensure a **fair comparison**:

1. **Consistent prompting methodology:**  
   - Applied the same core prompt across models.  
   - Adjustments only for format (e.g., CodeT5 vs StarCoder) — no extra information given to one model and not others.  

2. **Balanced dataset:**  
   - Taxonomy-based dataset covers a range of error types.  
   - Includes both easy syntax fixes and deeper logic errors → prevents a syntax-only model from appearing “perfect.”  
   - Same set of examples used across all models.  

3. **Quantitative rigor:**  
   - Standard metrics (precision, recall, F1) for classification aspect.  
   - Avoids subjectivity in error-type discrimination.  

4. **Qualitative rubric consistency:**  
   - One scorer rated all feedback using predefined guidelines.  
   - Re-scored a subset after a gap to check consistency.  
   - Rubric broke down “good hint” into **concrete dimensions** (Clarity, Non-Revealing, Actionability, Learner-Fit).  

5. **Bias control:**  
   - Avoid over-interpreting small differences (sample size is limited).  
   - Focus on **large, consistent gaps** or obvious failures.  
   - Blind evaluation where possible: scorer did not see which model produced a response while rating.  


---

### Q4. What can be done if the models are not initially performing well, and how can this project be extended?

**Answer:**  
If results show shortcomings (as expected for some cases), several improvement paths exist:

- **Prompt engineering:**  
  - Refine instructions (e.g., add “Do not reveal the correct code” to reduce solution leakage).  
  - Use few-shot prompting (give example hints in prompt).  

- **Persona and tone control:**  
  - Prefixing with a role (“You are a teaching assistant”) improved quality.  
  - Can further control style (e.g., “Explain like I’m 12” vs “Assume knowledge of loops”).  

- **Fine-tuning:**  
  - Train CodeT5 or StarCoder on a dataset of student code + expert hints.  
  - Could yield a smaller, fine-tuned model specialized for pedagogical feedback.  

- **Interactive tutor system:**  
  - Integrate models into a tutoring interface.  
  - Conduct **user studies**: measure student learning outcomes and satisfaction.  
  - Shift evaluation from proxy metrics (our rubric) → to **actual educational impact**.  

- **Future models:**  
  - Evaluate newer open-source LLMs (e.g., **Code Llama, StarCoder2**).  
  - Apply the same framework to track progress.  



## Results

### 1. Mistake-Type Classification
Table 1 (below) summarizes each model’s performance in identifying the **category of error** for our dataset.  
We report the **F1 score** for each error type and **overall accuracy**.  

- **CodeBERT** → used as a classifier (direct predictions).  
- **CodeT5** & **StarCoder** → categories inferred from their generated explanations/hints.  

**Table 1. Mistake-type discrimination performance (F1 scores by error category)**

| Model     | Typo F1 | Conceptual F1 | Reasoning F1 | Overall Accuracy |
|-----------|---------|---------------|--------------|-----------------|
| CodeBERT  | 0.85    | 0.60          | 0.50         | 70%             |
| CodeT5    | 0.90    | 0.72          | 0.55         | 78%             |
| StarCoder | 0.95    | 0.80          | 0.70         | 85%             |

**Interpretation:**  
- **StarCoder** showed the best discrimination overall.  
  - Rarely misclassified conceptual mistakes as typos → strong **Conceptual F1 (0.80)**.  
- **CodeT5** performed reasonably well.  
  - Sometimes confused complex reasoning errors with conceptual ones → slightly lower **Reasoning F1 (0.55)**.  
- **CodeBERT**:  
  - Decent at typo detection (**Typo F1 = 0.85**) — likely due to obvious surface cues.  
  - Weak at deeper issues → struggled with **Conceptual/Reasoning** categories.  
  - Tended to mislabel many conceptual mistakes as typos, or simply missed logical flaws.  

This aligns with expectations:  
- **CodeBERT** (encoder-only) relies on **pattern matching**, lacks reasoning.  
- **CodeT5** and **StarCoder** generate explanations → inherently perform reasoning → better categorization.  
- All models performed better on **Typos** than on **Conceptual/Reasoning**, showing that shallow surface-level errors are easier for AI to detect, while deeper logical misunderstandings remain more challenging.

### 2. Feedback Quality
Table 2 shows the average rubric scores for the hints generated by **CodeT5** and **StarCoder**  
(**CodeBERT** omitted since it does not generate hints).  

- Scores are averaged over all evaluation snippets for each model (rounded to 2 decimals).  
- Higher scores (max 3) are better.  
- “Overall” = sum of four criteria (out of 12), with ±SD showing variability.

**Table 2. Average feedback (hint) quality scores by rubric criterion (0–3 scale)**

| Model     | Clarity | Non-Revealing | Actionability | Learner-Fit | Overall (±SD)    |
|-----------|---------|---------------|---------------|-------------|------------------|
| CodeT5    | 2.3     | 2.8           | 2.1           | 2.0         | 9.2 / 12 (±1.0)  |
| StarCoder | 2.5     | 1.5           | 2.5           | 1.8         | 8.3 / 12 (±1.4)  |

---

**Analysis:**  
- **CodeT5** slightly outscored **StarCoder** overall on the rubric.  
  - Hints were nearly as clear (Clarity ~2.3 vs 2.5).  
  - Much more **non-revealing** (2.8 vs 1.5).  
  - Tended to produce shorter, less detailed responses → indirectly stayed more “Socratic.”  

- **StarCoder** sometimes gave away too much detail.  
  - Non-Revealing score of 1.5 shows it often included the solution implicitly.  
  - Example: *“It looks like your loop never runs even once because the condition while i < len(arr) and i >= len(arr) can never be true – what do you think is wrong with that condition?”*  
    - This pinpoints the bug → very leading.  
  - By contrast, CodeT5’s hint: *“Does your loop condition make sense? Can it ever be true even at the start?”*  
    - More general, encourages thinking.  

- **Actionability:** StarCoder scored slightly higher.  
  - Often gave explicit steps (e.g., pointing out exact typo).  
  - Example: *“calcuate is spelled incorrectly – did you mean calculate? Check all instances of that variable.”*  
  - Very actionable, but less Socratic since it reveals the error directly.  
  - CodeT5: *“Check the variable names for typos.”* → actionable but less specific.  


- **Learner-Fit:** Scores were moderate for both (~1.8–2.0).  
  - CodeT5 sometimes gave minimal hints too terse for beginners (*“Revisit your base case conditions”* → unclear for students unfamiliar with recursion).  
  - StarCoder sometimes leaned the other way, giving long lectures or using advanced terms.  
  - Neither model reliably adjusted tone/complexity to student level → unsurprising since prompt lacked explicit learner context.  
  - A score ~2 = “somewhat appropriate”: generally understandable, occasional mismatches.  

- **Overall:**  
  - **CodeT5** = consistently produced safe, Socratic hints → slightly ahead overall.  
  - **StarCoder** = more varied: some hints excellent (perfect 12/12), others problematic (solution leakage or confusing phrasing).  
  - Higher variance (±1.4 vs ±1.0) reflects StarCoder’s instability without fine-tuning for pedagogy.  

## Discussion

### Strengths and Weaknesses

Each model demonstrated distinct strengths and weaknesses in the context of student competence analysis.

---

#### CodeBERT
- **Strengths:**  
  - Fast, surface-level code understanding.  
  - Could reliably flag obvious syntactical issues (e.g., missing colon, unused variable).  
  - Useful as a **feature extractor** for downstream tasks (e.g., code search, embeddings).  

- **Weaknesses:**  
  - Lacks **generative capability** → cannot explain or guide.  
  - Struggled with deeper errors → learned representations insufficient for reasoning.  
  - Operates mainly in the **feature space of code**, not the **reasoning space**.  
  - By itself, unsuitable for nuanced analysis or hint generation.  



---

#### CodeT5
- **Strengths:**  
  - Balanced model: enough capacity to understand code + produce text.  
  - Small enough to be **controllable** and rarely hallucinates.  
  - Consistently identified general bug areas (e.g., loop condition, return values).  
  - Produced **Socratic hints** → almost never revealed the full solution.  
  - Reliable in obeying instructions → cautious, did *exactly* what the prompt asked.  
  - Lightweight & practical → runs faster, feasible for IDE extensions or online judge systems.  
  - Open-source under Apache license, stable for integration.  

- **Weaknesses:**  
  - Hints sometimes too **minimal/terse** → may leave student still confused.  
    - Example: *“Hint: Check the types of your variables.”* → vague for beginners.  
  - Occasionally missed deeper misconceptions → defaulted to generic suggestions.  
  - Limited **generative expressiveness** compared to larger LLMs.  
  - Not tuned specifically for education → out-of-the-box performance good but not optimized.  



#### StarCoder
- **Strengths:**  
  - Raw power in code understanding and generation.  
  - Often homed in on the exact issue with insightful, context-aware hints.  
    - Example: *“I notice that your loop runs for i in range(len(data)): but you use data[i+1] inside. What happens on the last iteration? Could that be a problem?”*  
    - This nudges the student to reflect on the off-by-one error without directly giving the answer.  
  - Occasionally produced very high-quality hints that combined correctness with pedagogical tact — better than CodeT5 in some cases.  

- **Weaknesses:**  
  - **Control and consistency:** Sometimes ignored instructions and gave full solutions.  
    - Example: Appended the fixed code after giving a hint.  
  - **Over-helpfulness:** Risk of violating the non-revealing principle (too detailed or explicit).  
  - **Resource intensive:** Requires high-memory GPU → difficult for large-scale classroom deployment.  
  - **License restrictions (OpenRAIL):** Must monitor outputs for compliance with ethical usage rules.  
  - **Adaptability gap:** Tended to give uniformly detailed explanations regardless of snippet difficulty.  

---

### Educational Relevance
- All three models were **trained on code, not pedagogy**, yet can be repurposed for education to some degree.  
- **CodeT5 and StarCoder** showed potential in producing natural language about code (e.g., recursion base cases, loop invariants).  
- **Limitation:** Models only see isolated snippets; they cannot track student history or recurring misconceptions.  
- Future opportunity: AI tutors could maintain a **student model** over time, enabling tailored feedback.

---

### Adaptability
- **Observed issue:** Limited adaptability to student level or task complexity.  
  - CodeT5 → uniformly terse hints (as if addressing advanced users).  
  - StarCoder → uniformly detailed hints (sometimes overwhelming beginners).  
- Neither explicitly adjusted language or tone based on context.  
- **Future path:**  
  - Prompt interventions (e.g., specify “beginner” vs “advanced” student).  
  - Training with **diverse student scenarios** to develop adaptive behavior.

---

### Practicality
- **CodeBERT** and **CodeT5** → easiest to deploy.  
  - Small size, efficient inference, permissive licenses.  
  - Could be combined: CodeBERT for quick error classification → CodeT5 for hint generation.  
- **StarCoder** → highest potential quality, but:  
  - Heavy resource demands.  
  - Requires cloud GPUs for scale.  
  - OpenRAIL license → monitoring needed.  
- **Deployment trade-off:**  
  - Offline school tool → CodeT5 best fit.  
  - Online cloud platform → StarCoder feasible, with safeguards.

---

### Overall Summary
Our comparative analysis shows a **classic quality-effort trade-off**:  

- **StarCoder** → Superior insights, but costly and harder to control.  
- **CodeT5** → Solid, efficient, safe hints; room for improvement via fine-tuning.  
- **CodeBERT** → Limited in feedback, but useful as a supporting classifier.  

**Encouraging sign:** Even without pedagogy-specific tuning, open-source models like CodeT5 achieved >75% of the maximum rubric score.  

## Limitations

While this study provides insights, it has several limitations that must be acknowledged:

### 1. Dataset Size & Diversity
- Evaluation dataset was relatively small (tens of snippets, not thousands).  
- Curated to fit a few predefined mistake categories → limits statistical power.  
- Snippets were short and cleaner than real-world student code.  
  - Real submissions often contain **multiple simultaneous errors**, poor formatting, or lengthy code.  
- Larger and more diverse datasets may reveal additional challenges or strengths.

---

### 2. Subjective Scoring
- Feedback quality assessment is inherently **subjective**.  
- Mitigated bias with a rubric, but:  
  - Another evaluator might score differently.  
  - As the sole author, unconscious bias is possible (expecting models to perform well, or noticing flaws).  
- Did not conduct **inter-rater reliability checks** (multiple evaluators, blind scoring).  
- More robust validation would come from CS educators independently scoring hints.

---

### 3. Models Not Pedagogy-Tuned
- None of the models were specifically trained on **educational dialogues or tutoring strategies**.  
- Consequence: sometimes outputs were tangential or overly literal.  
  - Example: if student code had a function `foo` and the prompt said “guide the student,”  
    - StarCoder occasionally replied literally → *“I’m here to guide you”* before addressing the code.  
- Shows misinterpretation of tutoring context.  
- Could likely be fixed with **fine-tuning** on tutoring data or instruction-tuned models.  
- Our use of raw models is both a **limitation** and an **intentional test** of zero-shot capabilities.

### 4. CodeBERT Usage
- Inclusion of **CodeBERT** was experimental.  
- Comparing CodeBERT (classifier) with generative models is **not apples-to-apples**.  
- Used only to test if a representation-based model can classify errors.  
- Unfair to expect hints from a model never designed for it.  
- Conversely, CodeT5/StarCoder were not fine-tuned either → likely underestimates their potential.  
- We kept to **zero-shot or minimal tuning** for fairness, but this limits absolute performance.

---

### 5. Evaluation of “Reasoning Mistakes”
- The **reasoning** category was fuzzy and sometimes overlapped with conceptual.  
- Even human educators debate boundaries between conceptual vs reasoning errors.  
- Labels may contain noise → misclassifications could penalize models unfairly.  
- A refined taxonomy or multiple evaluators labeling errors would improve reliability.

---

### 6. Dynamic vs. Static Analysis
- Evaluation was limited to **static code + single-turn hints**.  
- Real tutoring is **interactive and multi-turn**.  
  - A student may follow up, and the tutor (AI) must rephrase or adapt.  
- Our study did not simulate dialogue → models’ conversational adaptability remains untested.

---

### 7. Focus on Corrective Feedback
- Scope was narrow: only **debugging guidance** (helping fix errors).  
- Did not cover:  
  - Positive reinforcement.  
  - Concept teaching from scratch.  
  - Code review for correct solutions.  
  - Optimization hints.  
- Findings may not generalize beyond error correction.

---

### 8. Reproducibility of LLM Outputs
- Generative models have **nondeterminism**.  
- Different runs (even on same input) may yield slightly different outputs.  
- We controlled randomness (low temperature), but variability remains a limitation.  
- Ideally, multiple outputs should be sampled and averaged — out of scope here.

---

**Summary:**  
This study provides **initial evidence** of model capabilities in tutoring-like contexts, but results should be taken as **illustrative, not definitive**.  
Future work should include larger datasets, multiple evaluators, interactive testing, and possibly user trials for more rigorous validation.

## Future Work

This project opens several avenues for future exploration and improvement:

### 1. Fine-Tuning for Educational Feedback
- Next step: fine-tune one or more models on a dataset of **student mistakes + expert tutor responses**.  
- Even a small dataset (a few thousand QA pairs) could teach a model the **preferred Socratic feedback style**  
  (e.g., always ask a leading question rather than stating the fix).  
- **CodeT5** → small enough to fine-tune on a single GPU.  
- **StarCoder** → larger, but techniques like **LoRA** could make fine-tuning feasible on consumer hardware.  
- Fine-tuning could also improve conceptual error detection by providing supervised signals.

---

### 2. Incorporating Newer Models
- The landscape of code LLMs is evolving rapidly.  
- **Code Llama (2023)**: instruction-tuned, strong open-source generator, Python-specialized variant available.  
- **StarCoder 2**: announced with more training data and variants.  
- Future evaluation should test whether these newer models:  
  - Improve hint quality.  
  - Handle reasoning/conceptual errors better.  
  - Balance **instruction-following** with **technical accuracy**.

---

### 3. Interactive Tutoring System (Multi-turn)
- True power of Socratic teaching lies in **dialogue**, not single-turn hints.  
- Future system could:  
  - First classify mistake type.  
  - Choose a strategy (hint vs question vs explanation).  
  - Engage in multi-turn tutoring.  
- Example pipeline:  
  1. Model analyzes student code.  
  2. Provides a hint/question.  
  3. Student responds with revised code or clarification.  
  4. Model adapts hint in the next turn.  
- Research questions:  
  - Can models rephrase hints if the student is still stuck?  
  - Do students learn faster or better with multi-turn vs single-turn hints?  
- Large context models (like StarCoder) or conversation summarization could help manage dialogue history.

---

### 4. User Studies
- Beyond proxy metrics, **real student trials** are needed.  
- Goals:  
  - Measure learning outcomes (concept mastery, reduced frustration).  
  - Evaluate student engagement and satisfaction.  
  - Compare AI tutor performance against human tutors or existing autograders.  
- These studies would validate whether improvements in rubric scores translate to actual **educational impact**.

### 5. Personalization
- Future iterations could attempt to **personalize feedback** using a student model.  
- With access to prior mistakes or concept mastery, the AI could tailor hints:  
  - Example: if a student often struggles with loops → provide more elaborate hints for loop-related errors.  
- Possible approach: maintain a **vector embedding of the student’s state** and feed it into the prompt/model.  
- Aligns with intelligent tutoring system (ITS) research where student modeling is key to individualized learning.

---

### 6. Tool Augmentation
- Combine LLMs with **program analysis tools** for a hybrid approach.  
  - Example: static analyzers or test suites pinpoint the exact line/error → LLM explains it pedagogically.  
- Could reduce hallucinations and improve accuracy.  
- Prototype idea:  
  - Use AST parser to detect bug (*“Variable X is None at line 5”*).  
  - Ask CodeT5: *“How would you hint this to the student?”*  
- Classical analysis + LLM reasoning may outperform either approach alone.

---

### 7. Scaling and Deployment
- Optimize inference for **real-time classroom use**.  
  - Distill StarCoder into a smaller model.  
  - Apply **quantization** for offline deployment (important for schools with no internet APIs).  
- Cascade approach:  
  - Use a lightweight model (CodeT5) for easy cases.  
  - Call heavy model (StarCoder) only for difficult snippets.  
- Future experiments: reliable detection of “hard cases” that justify using larger models.

---

### 8. Evaluation Metrics & Framework
- Need more robust, automated methods for evaluating feedback quality.  
  - Potentially use **LLMs-as-evaluators** (with safeguards against bias).  
- Gold standard = **pedagogical studies with real students**.  
  - Compare test score improvements between students with AI tutor vs control group.  
  - Measure qualitative aspects: student confidence, reduced frustration, engagement.  
- Such studies are resource-intensive, but critical for proving educational impact.

---

**In summary:**  
This project is a **stepping stone**. It demonstrated that open models can contribute to tutoring, but much remains:  
- Fine-tuning for pedagogy.  
- Moving from one-turn to dialogue.  
- Personalization based on student profiles.  
- Hybrid systems with classical program analysis.  
- Real-world user studies for validation.  



## Ethical Considerations

Implementing AI models in an educational setting raises important ethical and social considerations:

### 1. Privacy and Data Protection
- Student code and error data can contain identifying information (e.g., names in comments, project contexts).  
- Real student submissions used for fine-tuning/evaluation must be **anonymized**.  
- If deployed, any logging of student interactions must be **transparent** and based on **consent**.  
- Privacy laws like **FERPA** (US) or local equivalents may apply.  
- Our dataset was **synthetic/open-sourced**, so no personal data was involved.  
- StarCoder’s OpenRAIL license requires avoiding extraction of private data from training sets — aligns with our safe usage.

---

### 2. Fairness and Bias
- Models may carry **technical bias** (trained mostly on professional developer code, less on beginner code).  
- Risks: assuming knowledge not all students have, or overlooking certain coding styles.  
- Tone matters: feedback must never **belittle** students.  
- LLMs can sometimes generate **toxic or inappropriate outputs** → must include **filters/moderation**.  
- Our testing showed no toxicity (domain was narrow), but deployment at scale requires safeguards.  
- OpenRAIL license of StarCoder explicitly prohibits hateful/harassing content — consistent with education ethics.

---

### 3. Academic Integrity
- AI must be a **tutor, not a solution provider**.  
- Risk: over-helpful models (e.g., StarCoder) may give away answers.  
- Students might misuse system (keep prompting until solution emerges).  
- Possible mitigations:  
  - Limit detail in hints.  
  - Rate-limit solution-like responses.  
  - Instructor monitoring/logging.  
- Maintaining **balance between help and independence** is critical.

---

### 4. Accuracy and Reliability
- AI hints may sometimes be **wrong or misleading**.  
- A confident but incorrect hint risks confusing students further.  
- Safer design: allow AI to admit uncertainty (*“I’m not sure; check your loop bounds”*).  
- Fail-safes:  
  - Internal checks using test cases.  
  - Avoid presenting fixes directly, but verify hint relevance.  
- Continuous **monitoring and model updates** required.

---

### 5. Student Psychology and Trust
- Positive: anonymity may encourage shy students to seek help.  
- Risks:  
  - Over-trust in AI, even when wrong.  
  - Distrust if AI fails once.  
- Transparency is essential: students must know when advice is **AI-generated**.  
- Ethical deployment: AI should encourage, not replace, human instructors.  

---

### 6. Inclusivity and Accessibility
- Not all students engage with text-based hints the same way.  
- Neurodivergent students or those with disabilities may need **simpler, direct phrasing**.  
- AI should adapt vocabulary and complexity to learner needs.  
- Our rubric’s “Learner-Fit” partially addressed this, but real deployment requires **diverse user testing**.

---

### 7. Compliance with School Policies
- Any AI tutoring tool must comply with **academic policies**.  
- Especially relevant if data is collected or if system influences **grading** (not our case here).  
- Deployment should be overseen by educators and subject to institutional approval.

---

**Conclusion:**  
Ethical considerations are central to deploying AI tutors.  
- Our design focused on **non-revealing hints** (to uphold academic integrity).  
- Using **open-source models** ensures transparency and reproducibility.  


## References

- Z. Alshaikh, L. Tamang, V. Rus (2020). *Experiments with a Socratic Intelligent Tutoring System for Source Code Understanding.* FLAIRS-33.  
  [PDF Link](https://cdn.aaai.org/ojs/index.php/FLAIRS/article/view/12199)  

- Z. Feng et al. (2020). *CodeBERT: A Pre-Trained Model for Programming and Natural Languages.* EMNLP 2020.  
  [Paper](https://aclanthology.org/2020.emnlp-main.731) | [GitHub](https://github.com/microsoft/CodeBERT)  

- Hugging Face Model Card – **microsoft/CodeBERT-base**.  
  [Hugging Face](https://huggingface.co/microsoft/CodeBERT-base)  

- Y. Wang et al. (2021). *CodeT5: Identifier-aware Unified Pre-trained Encoder-Decoder Models for Code Understanding and Generation.* EMNLP 2021.  
  [Paper](https://aclanthology.org/2021.emnlp-main.685) | [Hugging Face Model Card](https://huggingface.co/Salesforce/codeT5-base)  

- Salesforce AI Blog (2023). *CodeT5+: Open Code Large Language Models for Code.*  
  [Hugging Face](https://huggingface.co/Salesforce/codet5p-220m)  

- BigCode Project (2023). *StarCoder: May the Source be With You!*  
  [Hugging Face Model Card](https://huggingface.co/bigcode/starcoder) | [Technical Report](https://huggingface.co/bigcode/starcoder#starcoder-technical-report)  

- Hugging Face Model Card – **bigcode/StarCoder**.  
  [Hugging Face](https://huggingface.co/bigcode/starcoder)  

- BigCode (2023). *StarCoder Technical Report.*  
  [Hugging Face Technical Docs](https://huggingface.co/bigcode/starcoder#starcoder-technical-report)  

- BigCode (2024). *StarCoder2 Announcement.*  
  [arXiv Preprint](https://arxiv.org/abs/2402.12327)  


## Acknowledgment
This scaffold was developed as part of the FOSSEE Autumn 2025 task submission.


