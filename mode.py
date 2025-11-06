def mode(numbers):
    counts = {}
    best_value = None
    best_count = 0
    for x in numbers:
        c = counts.get(x, 0) + 1
        counts[x] = c
        if c > best_count:
            best_count = c
            best_value = x
    return best_value


