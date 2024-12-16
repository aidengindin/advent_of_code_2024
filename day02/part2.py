# def is_safe(report):
#     prev = report[0]
#     maybe_increasing = True
#     maybe_decreasing = True
#     needs_retroactive_dampening = False
#     dampened = False

#     # need to handle: 1st 2 increase/decrease safely, then opposite direction for the rest
#     # ie 1st level dampened
#     for i in range(1, len(report)):
#         current = report[i]
#         current_dampened = False  # whether this level is being dampened

#         # handle retroactive dampening
#         if i == 2:
#             if (report[0] < report[1] and report[1] > report[2]) or (report[0] > report[1] and report[1] < report[2]):
#                 maybe_decreasing = True
#                 maybe_increasing = True
#                 needs_retroactive_dampening = True
#         if i == 3 and needs_retroactive_dampening:
#             increasing_first_dampened = all(i < j for i, j in zip(report[1:3], report[2:4])) and report[0] > report[1]
#             decreasing_first_dampened = all(i > j for i, j in zip(report[1:3], report[2:4])) and report[0] < report[1]
#             increasing_second_dampened = all(i < j for i, j in zip([report[0], report[2]], report[2:4])) and report[1] > report[2]
#             decreasing_second_dampened = all(i > j for i, j in zip([report[0], report[2]], report[2:4])) and report[1] < report[2]
#             if increasing_first_dampened or decreasing_first_dampened or increasing_second_dampened or decreasing_second_dampened:
#                 dampened = True
#             else:
#                 return False
#             needs_retroactive_dampening = False
        
#         # handle monotonicity violations
#         if not maybe_increasing and current >= prev:
#             if not dampened:
#                 current_dampened = True
#             else:
#                 return False
#         elif not maybe_decreasing and current <= prev:
#             if not dampened:
#                 current_dampened = True
#             else:
#                 return False

#         # handle gradualness violations (and equality)
#         diff = abs(current - prev)
#         if diff < 1 or diff > 3:
#             if not dampened:
#                 current_dampened = True
#             else:
#                 return False

#         # set maybe_increasing and maybe_decreasing if not dampening
#         if current > prev and not current_dampened and not needs_retroactive_dampening:
#             maybe_decreasing = False
#         elif current < prev and not current_dampened and not needs_retroactive_dampening:
#             maybe_increasing = False

#         if not current_dampened:
#             prev = current
#         dampened = dampened or current_dampened

#     return True

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

def is_safe_without_dampening(report):
    if len(report) == 0:
        return True
    return (is_increasing(report) or is_decreasing(report)) and is_gradual(report)

def is_safe_with_dampening(report):
    for i in range(len(report)):
        if is_safe_without_dampening(report[:i] + report[i+1:]):
            return True
    return False

is_safe = is_safe_with_dampening

with open("day2/input.txt") as f:
    reports = [list(map(int, line.split())) for line in f.readlines()]
    num_safe = sum([1 if is_safe(report) else 0 for report in reports])
    print(num_safe)
