# Intent: copy a list and modify the copy
a = [1, 2, 3]
b = a                      # aliasing, not an actual copy
b.append(4)
print(a, b)                # both change; misunderstanding mutability/aliasing
