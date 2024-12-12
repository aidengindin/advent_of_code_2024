def parse(lines):
    result = []
    for line in lines:
        key, values = line.strip().split(': ')
        key = int(key)
        values = [int(x) for x in values.split()]
        result.append((key, values))
    return result

def evaluate(result, numbers, acc=None):
    if acc == None:
        acc = numbers[0]
        numbers = numbers[1:]
    if len(numbers) == 0:
        return acc == result
    next = numbers[0]
    add = acc + next
    multiply = acc * next
    concatenate = int(str(acc) + str(next))
    plausible = [x for x in [add, multiply, concatenate] if x <= result]
    if len(plausible) == 0:
        return False
    return any([evaluate(result, numbers[1:], x) for x in plausible])

def possible_sum(equations):
    return sum([equation[0] for equation in equations if evaluate(equation[0], equation[1])])

with open("day7/input.txt", "r") as f:
    lines = f.readlines()
    equations = parse(lines)
    print(possible_sum(equations))
