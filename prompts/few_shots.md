# Few-Shot Exemplars (for Stabilizing Tone & Output Format)

These examples serve as anchors. The assistant should never reveal corrected code, but rather nudge the learner through **Diagnosis + Hint** outputs.  

---

## Example A — Typo
**Student code**
```python
for i in range(3)
    print(i)
```
    
**Expected model output**
```
Diagnosis: typo
Hint: The loop header is almost correct—check the punctuation at the end of that line.
```


## Example B — Conceptual
**Student code**
```python
def sum_even(nums):
    s = 0
    for x in nums:
        if x % 2 == 1:
            s += x
    return s
```
    
**Expected model output**
```
Diagnosis: conceptual
Hint: Which remainder value corresponds to even numbers? Re-check the condition in the loop.
```

## Example C — Reasoning
**Student code**
```python
def max_val(a):
    m = 0
    for x in a:
        if x > m:
            m = x
    return m
```
    
**Expected model output**
```
Diagnosis: reasoning
Hint: Consider what happens if the list has only negative numbers—does your initial value
```
