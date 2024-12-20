import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
    
    def push(self, element, priority):
        heapq.heappush(self._queue, (priority, element))

    def pop(self):
        return heapq.heappop(self._queue)[1]

    def empty(self):
        return len(self._queue) == 0

def adjacent(tile, walls):
    x, y = tile
    return {tup for tup in {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} if tup not in walls}

def manhattan_distance(tile1, tile2):
    x1, y1 = tile1
    x2, y2 = tile2
    return abs(x1 - x2) + abs(y1 - y2)

def parse(lines):
    start = None
    end = None
    walls = set()
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            tile = (j, i)
            char = lines[i][j]
            if char == "#":
                walls.add(tile)
            elif char == "S":
                start = tile
            elif char == "E":
                end = tile
    return start, end, walls

def search(start, end, walls):
    heuristic = lambda tile: manhattan_distance(tile, end)
    frontier = PriorityQueue()
    frontier.push(start, heuristic(start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.pop()
        if current == end:
            break
        for next in adjacent(current, walls):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next)
                frontier.push(next, priority)
                came_from[next] = current
    
    return cost_so_far[end], retrace(start, end, came_from)

def retrace(start, end, came_from):
    current = end
    out = []
    while current != start:
        out = [current] + out
        current = came_from[current]
    return [start] + out

def get_cheats(path, walls):
    cheats_by_time_saved = dict()
    path_set = set(path)  # lets us do O(1) lookups to determine whether a tile is in the path
    for tile in path:
        potential = filter(lambda t: t in path_set, two_away(tile))
        for potential_tile in potential:
            start_index = path.index(tile)
            end_index = path.index(potential_tile)
            if end_index > start_index and has_intermediate_wall(tile, potential_tile, walls):
                ps_saved = len(path[start_index:end_index]) - 2
                if ps_saved in cheats_by_time_saved:
                    cheats_by_time_saved[ps_saved] += 1
                else:
                    cheats_by_time_saved[ps_saved] = 1
    return cheats_by_time_saved

def two_away(tile):
    x, y = tile
    return {(x - 2, y), (x + 2, y), (x, y - 2), (x, y + 2)}

def has_intermediate_wall(tile1, tile2, walls):
    # assumes tile1, tile2 are 2 away from each other
    x1, y1 = tile1
    x2, y2 = tile2
    x_mid = min(x1, x2) + 1
    y_mid = min(y1, y2) + 1
    if x1 == x2:
        return (x1, y_mid) in walls
    return (x_mid, y1) in walls

def num_cheats_over_n(cheats_by_time_saved, n):
    return sum([count for time_saved, count in cheats_by_time_saved.items() if time_saved >= n])

with open("day20/input.txt", "r") as f:
    lines = f.readlines()
    start, end, walls = parse(lines)
    cost, path = search(start, end, walls)
    cheats = get_cheats(path, walls)
    num = num_cheats_over_n(cheats, 100)
    print(num)
