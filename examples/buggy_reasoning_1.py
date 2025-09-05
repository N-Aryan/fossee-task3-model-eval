# Intent: return max element of a list
def my_max(arr):
    max_val = 0            # wrong initialization: fails for all-negative lists
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val
