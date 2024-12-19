def parse(lines):
    towels = {towel for towel in lines[0].strip().split(", ")}
    designs = {line.strip() for line in lines[2:]}
    return towels, designs

def is_possible(towels, design, max_towel_length, memo):
    if design in memo:
        return memo[design]
    if len(design) == 0:
        return False
    for i in range(1, max_towel_length + 1):
        if design[:i] in towels and (len(design) == i or is_possible(towels, design[i:], max_towel_length, memo)):
            memo[design] = True
            return True
    memo[design] = False
    return False

def num_possible(towels, designs):
    max_towel_length = max({len(towel) for towel in towels})
    memo = dict()
    return sum(1 for design in designs if is_possible(towels, design, max_towel_length, memo))

with open("day19/input.txt", "r") as f:
    lines = f.readlines()
    towels, designs = parse(lines)
    num = num_possible(towels, designs)
    print(num)
