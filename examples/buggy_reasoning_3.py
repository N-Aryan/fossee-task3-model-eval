# Intent: remove all zeros from a list
data = [0, 1, 0, 2, 0, 3]
for i, x in enumerate(data):
    if x == 0:
        data.pop(i)               # mutating while iterating → skips elements
print(data)
