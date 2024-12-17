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

def get_num_sides(region, garden):
    # strategy:
    # for each plot, get the direction of each exposed side (similar to perimeter but noting direction)
    # if 2 plots are next to each other in the relevant direction and have the same direction exposed,
    # they are part of the same side
    plant = region[0]
    plots = region[1]
    size = len(garden)
    sides = []  # {(direction, {point1, point2, ...}), ...}
    points_on_side = []  # {(point, direction), (point, direction)}
    for plot in plots:
        i = plot[0]
        j = plot[1]
        if i == 0 or garden[i - 1][j] != plant:
            points_on_side.append((plot, "U"))
        if i == size - 1 or garden[i + 1][j] != plant:
            points_on_side.append((plot, "D"))
        if j == 0 or garden[i][j - 1] != plant:
            points_on_side.append((plot, "L"))
        if j == size - 1 or garden[i][j + 1] != plant:
            points_on_side.append((plot, "R"))
    points_on_side.sort(key=lambda x: x[0][0])
    points_on_side.sort(key=lambda x: x[0][1])
    for plot, direction in points_on_side:
        possible_sides = list(filter(lambda side: side[0] == direction, sides))
        added = False
        for _, side_plots in possible_sides:
            if any([adjacent_and_aligned(plot, side_plot, direction) for side_plot in side_plots]):
                side_plots.add(plot)
                added = True
                break
        if not added:
            sides.append((direction, {plot}))
    return len(sides)

# whether 2 plots are adjacent, and also have an edge in the same direction
def adjacent_and_aligned(plot1, plot2, direction):
    if direction in ["U", "D"]:
        return plot1[0] == plot2[0] and abs(plot1[1] - plot2[1]) == 1
    if direction in ["L", "R"]:
        return plot1[1] == plot2[1] and abs(plot1[0] - plot2[0]) == 1
    raise ValueError("direction must be U, D, L, or R")

def get_cost(regions, garden):
    cost = 0
    for region in regions:
        area = get_area(region)
        num_sides = get_num_sides(region, garden)
        cost += area * num_sides
    return cost

with open("day12/input.txt", "r") as f:
    lines = f.readlines()
    garden = parse(lines)
    regions = get_regions(garden)
    cost = get_cost(regions, garden)
    print(cost)
