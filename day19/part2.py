def parse(lines):
    towels = {towel for towel in lines[0].strip().split(", ")}
    designs = {line.strip() for line in lines[2:]}
    return towels, designs

def possible_arrangements(towels, design, max_towel_length, memo):
    if design in memo:
        return memo[design]
    if len(design) == 0:
        return 0
    for i in range(1, min(len(design), max_towel_length) + 1):
        current = design[:i]
        if current in towels:
            if len(design) == i:
                update_memo(memo, design, 1)
            else:
                rhs_arrangements = possible_arrangements(towels, design[i:], max_towel_length, memo)
                if rhs_arrangements > 0:
                    update_memo(memo, design, rhs_arrangements)
    if design not in memo:
        memo[design] = 0
    return memo[design]

def update_memo(memo, design, arrangements):
    if design in memo:
        memo[design] += arrangements
    else:
        memo[design] = arrangements

def num_possible(towels, designs):
    max_towel_length = max({len(towel) for towel in towels})
    memo = dict()
    return sum(possible_arrangements(towels, design, max_towel_length, memo) for design in designs)

with open("day19/input.txt", "r") as f:
    lines = f.readlines()
    towels, designs = parse(lines)
    num = num_possible(towels, designs)
    print(num)
