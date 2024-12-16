def parse(lines):
    map = []
    for line in lines:
        line = line.strip()
        positions = []
        for position in line:
            positions.append(int(position))
        map.append(positions)
    return map

def get_trailheads(map):
    return [(i, j) for i in range(len(map)) for j in range(len(map[i])) if map[i][j] == 0]

def get_adjacent(position, size):
    i = position[0]
    j = position[1]
    return list(filter(lambda pos: 0 <= pos[0] and pos[0] < size and 0 <= pos[1] and pos[1] < size, [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]))

def get_height(position, map):
    return map[position[0]][position[1]]

def get_score(trailhead, map):
    reachable_nines = set()
    size = len(map)
    next = [adjacent for adjacent in get_adjacent(trailhead, size) if get_height(adjacent, map) == 1]
    while len(next) > 0:
        position = next.pop(0)
        height = get_height(position, map)
        if height == 9:
            reachable_nines.add(position)
        else:
            next += [adjacent for adjacent in get_adjacent(position, size) if get_height(adjacent, map) == height + 1]
    score = len(reachable_nines)
    return score

with open("day10/input.txt", "r") as f:
    lines = f.readlines()
    map = parse(lines)
    trailheads = get_trailheads(map)
    total_score = sum([get_score(trailhead, map) for trailhead in trailheads])
    print(total_score)
