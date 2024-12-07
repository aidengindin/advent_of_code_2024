def is_safe(report):
    return (is_increasing(report) or is_decreasing(report)) and is_gradual(report)

def is_increasing(report):
    prev = report[0]
    for i in range(1, len(report)):
        if report[i] <= prev:
            return False
        prev = report[i]
    return True

def is_decreasing(report):
    prev = report[0]
    for i in range(1, len(report)):
        if report[i] >= prev:
            return False
        prev = report[i]
    return True

def is_gradual(report):
    prev = report[0]
    for i in range(1, len(report)):
        diff = abs(report[i] - prev)
        if diff < 1 or diff > 3:
            return False
        prev = report[i]
    return True

with open("day2/input.txt") as f:
    reports = [list(map(int, line.split())) for line in f.readlines()]
    num_safe = sum([1 if is_safe(report) else 0 for report in reports])
    test = [15, 12, 11, 9, 6, 4]
    # print(is_decreasing(test))
    print(num_safe)

# 1 3 2 4 5 - can removed 2nd or 3rd
# 1 3 
