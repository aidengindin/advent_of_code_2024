import itertools


class AntennaMap():
    def __init__(self, xsize, ysize, frequencies) -> None:
        self.xsize = xsize
        self.ysize = ysize
        self.frequencies = frequencies

def get_antennas(lines):
    frequencies = {}
    for i in range(len(lines)):
        line = lines[i].strip()
        for j in range(len(line)):
            char = lines[i][j]
            if char != ".":
                if char not in frequencies:
                    frequencies[char] = {(j, i)}  # this time, i'm swapping the coordinates here to make life easier later
                else:
                    frequencies[char].add((j, i))
    return AntennaMap(len(lines[0].strip()), len(lines), frequencies)

def in_map(coord, map):
    x = coord[0]
    y = coord[1]
    return 0 <= x and x < map.xsize and 0 <= y and y < map.ysize

def antinodes(antenna_map):
    antis = set()
    for antennas in antenna_map.frequencies.values():
        pairs = itertools.combinations(antennas, 2)
        for pair in pairs:
            first = pair[0]
            second = pair[1]
            xdiff = first[0] - second[0]
            ydiff = first[1] - second[1]
            first_anti = (first[0] + xdiff, first[1] + ydiff)
            second_anti = (second[0] - xdiff, second[1] - ydiff)
            antis.update([first_anti, second_anti])
    valid = {anti for anti in antis if in_map(anti, antenna_map)}
    return len(valid)

with open("day8/input.txt", "r") as f:
    lines = f.readlines()
    map = get_antennas(lines)
    count = antinodes(map)
    print(count)
