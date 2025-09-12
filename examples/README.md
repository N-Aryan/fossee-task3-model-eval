# Examples Dataset

This folder contains **buggy Python code snippets** for evaluation.

- **Buggy files**: `bug1.py` … `bug9.py` (each snippet has one intentional mistake).  
- **labels.csv**: Maps each file to its gold label.  
  - Columns: `filename, gold_label`  
  - Labels used:  
    - `typo` → surface-level syntax or slip.  
    - `conceptual` → misunderstanding of a programming construct.  
    - `reasoning` → flawed logic or problem approach.  

These examples are intentionally minimal and educational.  
They illustrate how models are expected to produce both a **diagnosis** and a **non-revealing hint**.


## Sample labels.csv

| filename | gold_label   |
|----------|--------------|
| bug1.py  | typo         |
| bug2.py  | conceptual   |
| bug3.py  | reasoning    |


