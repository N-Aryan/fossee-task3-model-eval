# Intent: count even numbers in a list
def count_even(arr):
    count = 0
    for x in arr:
        if x % 2 == 1:     # conceptual error: this checks odd numbers
            count += 1
    return count
