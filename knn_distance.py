def knn_distance(arr, q, k):
    pairs = [(abs(x - q), x) for x in arr]
    left = 0
    right = len(pairs) - 1
    target = k - 1
    while True:
        if left == right:
            d, v = pairs[target]
            return d, v
        pivot_index = (left + right) // 2
        pivot_value = pairs[pivot_index][0]
        i = left
        j = right
        while i <= j:
            while pairs[i][0] < pivot_value:
                i += 1
            while pairs[j][0] > pivot_value:
                j -= 1
            if i <= j:
                pairs[i], pairs[j] = pairs[j], pairs[i]
                i += 1
                j -= 1
        if target <= j:
            right = j
        elif target >= i:
            left = i
        else:
            d, v = pairs[target]
            return d, v


