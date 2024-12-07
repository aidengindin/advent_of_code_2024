import re

with open("day3/input.txt", "r") as f:
    memory = "".join(f.readlines())
    pattern = r"mul\([0-9]{1,3},[0-9]{1,3}\)"
    matches = re.findall(pattern, memory)
    sum = 0
    for match in matches:
        numbers = [int(s.strip("mul()")) for s in match.split(",")]
        sum += numbers[0] * numbers[1]
    print(sum)
