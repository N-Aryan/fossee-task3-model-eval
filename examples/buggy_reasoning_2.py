# Intent: binary search (arr sorted ascending), return index or -1
def bsearch(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo < hi:                 # off-by-one: may skip final candidate
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            hi = mid - 1          # wrong direction update
        else:
            lo = mid + 1
    return -1
