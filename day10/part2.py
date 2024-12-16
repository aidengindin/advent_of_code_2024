def parse(lines):
    topo_map = []
    for line in lines:
        line = line.strip()
        positions = []
        for position in line:
            positions.append(int(position))
        topo_map.append(positions)
    return topo_map

def get_trailheads(topo_map):
    return [(i, j) for i in range(len(topo_map)) for j in range(len(topo_map[i])) if topo_map[i][j] == 0]

def get_adjacent(position, size):
    i = position[0]
    j = position[1]
    return list(filter(lambda pos: 0 <= pos[0] and pos[0] < size and 0 <= pos[1] and pos[1] < size, [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]))

def get_height(position, topo_map):
    return topo_map[position[0]][position[1]]

def get_rating(trailhead, topo_map):
    size = len(topo_map)
    current_height = get_height(trailhead, topo_map)
    if current_height == 9:
        return 1
    next = [adjacent for adjacent in get_adjacent(trailhead, size) if get_height(adjacent, topo_map) == current_height + 1]
    if len(next) == 0:
        return 0
    return sum(map(lambda position: get_rating(position, topo_map), next))

with open("day10/input.txt", "r") as f:
    lines = f.readlines()
    topo_map = parse(lines)
    trailheads = get_trailheads(topo_map)
    total_score = sum([get_rating(trailhead, topo_map) for trailhead in trailheads])
    print(total_score)
