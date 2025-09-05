# Intent: factorial(n) using recursion
def fact(n):
    # missing proper base case; infinite recursion for n == 0
    return n * fact(n - 1)

print(fact(5))
