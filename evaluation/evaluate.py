"""
Evaluation scaffold.
- Loads examples/ and labels.csv
- Builds prompts using prompts/ system files + policy + (optional) few-shots
- (Placeholder) calls `call_model()`; you can replace with real inference
- Saves raw outputs and a predictions CSV for downstream metrics

Usage:
  python evaluation/evaluate.py --model codet5 --level beginner
  python evaluation/evaluate.py --model starcoder --level advanced
"""

import argparse, csv, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
EX_DIR = ROOT / "examples"
PR_DIR = ROOT / "prompts"
OUT_DIR = ROOT / "evaluation" / "results"

def read_labels():
    with open(EX_DIR / "labels.csv", newline="") as f:
        return {row["filename"]: row["label"] for row in csv.DictReader(f)}

def read_txt(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8").strip()

def build_prompt(level: str, code: str, use_fewshots: bool = False) -> str:
    sysfile = "system_prompt_beginner.txt" if level == "beginner" else "system_prompt_advanced.txt"
    role = read_txt(PR_DIR / sysfile)
    policy = read_txt(PR_DIR / "policy_non_revealing.txt")
    prompt = [role, "", "Follow the Non-Revealing Feedback Policy:", policy, "", "Student code:", "```python", code, "```", "", "Output format:", "Diagnosis: <typo|conceptual|reasoning|uncertain>", "Hint: <one or two sentences>"]
    if use_fewshots and (PR_DIR / "few_shots.md").exists():
        prompt.insert(0, read_txt(PR_DIR / "few_shots.md"))
    return "\n".join(prompt)

def call_model(model_name: str, prompt: str) -> str:
    """
    TODO: Replace with actual inference (HF pipeline / API).
    For now we return a placeholder so the pipeline runs.
    Output must respect the contract (Diagnosis + Hint lines).
    """
    return "Diagnosis: uncertain\nHint: Placeholder output. Replace `call_model` with real inference."

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)  # codet5 | codebert | starcoder | custom
    parser.add_argument("--level", default="beginner", choices=["beginner", "advanced"])
    parser.add_argument("--fewshots", action="store_true", help="prepend few-shot exemplars")
    args = parser.parse_args()

    labels = read_labels()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "raw" / args.model).mkdir(parents=True, exist_ok=True)

    rows = []
    for fname, gold in labels.items():
        code = read_txt(EX_DIR / fname)
        prompt = build_prompt(args.level, code, args.fewshots)
        output = call_model(args.model, prompt)

        # save raw output
        (OUT_DIR / "raw" / args.model / f"{fname}.txt").write_text(output, encoding="utf-8")

        rows.append({"filename": fname, "gold_label": gold, "model_output": output})

    # write predictions log
    pred_csv = OUT_DIR / f"predictions_{args.model}.csv"
    with open(pred_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["filename", "gold_label", "model_output"])
        w.writeheader()
        w.writerows(rows)

    print(f"Saved raw outputs to {OUT_DIR / 'raw' / args.model}")
    print(f"Wrote predictions to {pred_csv}")

if __name__ == "__main__":
    main()
