def swap_sum(A, B):
    sumA = sum(A)
    sumB = sum(B)
    diff = sumB - sumA - 10
    if diff % 2 != 0:
        return None
    target = diff // 2
    i, j = 0, 0
    n, m = len(A), len(B)
    while i < n and j < m:
        cur = B[j] - A[i]
        if cur == target:
            return (i, j)
        if cur < target:
            j += 1
        else:
            i += 1
    return None


