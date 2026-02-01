def add(a, b):
    return a + b

def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

result = add(5, 3)                    # 8
minimum, maximum, total = get_stats([1, 2, 3, 4, 5])
