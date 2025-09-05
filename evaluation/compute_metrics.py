"""
Compute discrimination metrics from predictions CSV.
Parses the 'Diagnosis: <label>' line in model_output and compares with gold.

Usage:
  python evaluation/compute_metrics.py --pred evaluation/results/predictions_codet5.csv
"""

import argparse, csv, json, re, collections, pathlib

LABELS = ["typo", "conceptual", "reasoning", "uncertain"]

def parse_diag(text: str) -> str:
    m = re.search(r"(?i)^diagnosis\s*:\s*([a-z]+)", text, re.M)
    if not m: return "uncertain"
    label = m.group(1).lower()
    return label if label in LABELS else "uncertain"

def metrics_from_counts(tp, fp, fn):
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec  = tp / (tp + fn) if (tp + fn) else 0.0
    f1   = (2*prec*rec)/(prec+rec) if (prec+rec) else 0.0
    return prec, rec, f1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", required=True)
    args = ap.parse_args()

    # confusion counts
    idx = {lbl:i for i,lbl in enumerate(LABELS)}
    cm = [[0]*len(LABELS) for _ in LABELS]

    with open(args.pred, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            gold = row["gold_label"].strip().lower()
            pred = parse_diag(row["model_output"])
            if gold not in idx: gold = "uncertain"
            cm[idx[gold]][idx[pred]] += 1

    # per-class metrics
    per = {}
    for l, lbl in enumerate(LABELS):
        tp = cm[l][l]
        fp = sum(cm[r][l] for r in range(len(LABELS)) if r != l)
        fn = sum(cm[l][c] for c in range(len(LABELS)) if c != l)
        prec, rec, f1 = metrics_from_counts(tp, fp, fn)
        per[lbl] = {"precision": round(prec,3), "recall": round(rec,3), "f1": round(f1,3)}

    overall_acc = sum(cm[i][i] for i in range(len(LABELS))) / max(1, sum(sum(r) for r in cm))

    out = {
        "labels": LABELS,
        "confusion_matrix": cm,
        "per_class": per,
        "overall_accuracy": round(overall_acc,3),
    }

    out_path = pathlib.Path(args.pred).with_suffix("").parent / f"metrics_{pathlib.Path(args.pred).stem.split('_',1)[-1]}.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    # pretty print
    print("Confusion Matrix (rows=gold, cols=pred):")
    hdr = ["gold\\pred"] + LABELS
    print("\t".join(hdr))
    for i, row in enumerate(cm):
        print("\t".join([LABELS[i]] + [str(x) for x in row]))
    print("\nPer-class metrics:")
    for k,v in per.items():
        print(f"{k:11s}  P={v['precision']:.3f}  R={v['recall']:.3f}  F1={v['f1']:.3f}")
    print(f"\nOverall accuracy: {overall_acc:.3f}")
    print(f"Saved metrics JSON → {out_path}")

if __name__ == "__main__":
    main()
