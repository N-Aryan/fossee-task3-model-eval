# Intent: sum a list
nums = [1, 2, 3, 4]
totl = 0
for n in nums:
    total += n             # NameError: 'total' vs 'totl' (misspelling)
print(total)
