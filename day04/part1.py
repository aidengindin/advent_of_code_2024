def num_horizontal(lines):
    num = 0
    for line in lines:
        for j in range(len(lines)):
            if line[j] == "X":
                # look left
                if j >= 3 and line[j - 1] == "M" and line[j - 2] == "A" and line[j - 3] == "S":
                    num += 1
                # look right
                if j <= len(line) - 4 and line[j + 1] == "M" and line[j + 2] == "A" and line[j + 3] == "S":
                    num += 1
    return num

def num_vertical(lines):
    transposed = list(map(lambda line: "".join(map(str, line)), zip(*lines)))
    return num_horizontal(transposed)

def num_diagonal(lines):
    num = 0
    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            letter = line[j]
            if letter == "X":
                num += up_left(lines, i, j) + up_right(lines, i, j) + down_left(lines, i, j) + down_right(lines, i, j)
    return num

def up_left(lines, i, j):
    if i < 3 or j < 3:
        return 0
    if lines[i - 1][j - 1] == "M" and lines[i - 2][j - 2] == "A" and lines[i - 3][j - 3] == "S":
        return 1
    return 0

def up_right(lines, i, j):
    if i < 3 or j > len(lines[i]) - 4:
        return 0
    if lines[i - 1][j + 1] == "M" and lines[i - 2][j + 2] == "A" and lines[i - 3][j + 3] == "S":
        return 1
    return 0

def down_left(lines, i, j):
    if i > len(lines) - 4 or j < 3:
        return 0
    if lines[i + 1][j - 1] == "M" and lines[i + 2][j - 2] == "A" and lines[i + 3][j - 3] == "S":
        return 1
    return 0

def down_right(lines, i, j):
    if i > len(lines) - 4 or j > len(lines[i]) - 4:
        return 0
    if lines[i + 1][j + 1] == "M" and lines[i + 2][j + 2] == "A" and lines[i + 3][j + 3] == "S":
        return 1
    return 0

with open("day4/input.txt", "r") as f:
    lines = f.readlines()
    horizontal = num_horizontal(lines)
    vertical = num_vertical(lines)
    diagonal = num_diagonal(lines)
    xmas_count = horizontal + vertical + diagonal
    print(xmas_count)

# test:
# horizontal: 5
# vertical: 3
# diagonal: 10