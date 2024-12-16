def xmas_count(lines):
    count = 0
    for i in range(len(lines) - 2):
        line = lines[i]
        for j in range(len(line) - 2):
            char = line[j]
            if char == "M":
                common = lines[i+1][j+1] == "A" and lines[i+2][j+2] == "S"
                horizontal = lines[i+2][j] == "M" and lines[i][j+2] == "S"
                vertical = lines[i+2][j] == "S" and lines[i][j+2] == "M"
                if common and (horizontal or vertical):
                    count += 1
            elif char == "S":
                common = lines[i+1][j+1] == "A" and lines[i+2][j+2] == "M"
                horizontal = lines[i+2][j] == "S" and lines[i][j+2] == "M"
                vertical = lines[i+2][j] == "M" and lines[i][j+2] == "S"
                if common and (horizontal or vertical):
                    count += 1
    return count


with open("day4/input.txt", "r") as f:
    lines = f.readlines()
    count = xmas_count(lines)
    print(count)

# test:
# horizontal: 5
# vertical: 3
# diagonal: 10