def parse(lines):
    return [list(line.strip()) for line in lines]

def in_region(i, j, regions):
    return any({True for region in regions if (i, j) in region[1]})

def get_adjacent(i, j, size):
    return set(filter(lambda pos: 0 <= pos[0] and pos[0] < size and 0 <= pos[1] and pos[1] < size, [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]))

def get_regions(garden):
    size = len(garden)
    regions = set()
    for i in range(len(garden)):
        for j in range(len(garden[i])):
            plant = garden[i][j]
            if in_region(i, j, regions):
                continue
            plots = {(i, j)}
            next = {adjacent for adjacent in get_adjacent(i, j, size) if garden[adjacent[0]][adjacent[1]] == plant}
            while len(next) > 0:
                plot = next.pop()
                plots.add(plot)
                next.update({adjacent for adjacent in get_adjacent(plot[0], plot[1], size) if garden[adjacent[0]][adjacent[1]] == plant and adjacent not in plots})
            regions.add((plant, frozenset(plots)))
    return regions

def get_area(region):
    return len(region[1])

def get_perimeter(region, garden):
    plant = region[0]
    plots = region[1]
    perimeter = 0
    size = len(garden)
    for plot in plots:
        adjacent = [adjacent for adjacent in get_adjacent(plot[0], plot[1], size) if garden[adjacent[0]][adjacent[1]] == plant]
        perimeter += 4 - len(adjacent)
    return perimeter

def get_cost(regions, garden):
    cost = 0
    for region in regions:
        area = get_area(region)
        perimeter = get_perimeter(region, garden)
        cost += area * perimeter
    return cost

with open("day12/input.txt", "r") as f:
    lines = f.readlines()
    garden = parse(lines)
    regions = get_regions(garden)
    cost = get_cost(regions, garden)
    print(cost)
