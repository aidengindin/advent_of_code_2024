import re

with open("day3/input.txt", "r") as f:
    memory = "".join(f.readlines())
    pattern = r"mul\([0-9]{1,3},[0-9]{1,3}\)|do(?:|n\'t)\(\)"
    matches = re.findall(pattern, memory)
    enable = True
    sum = 0
    for match in matches:
        if match == "do()":
            enable = True
        elif match == "don't()":
            enable = False
        elif enable:
            numbers = [int(s.strip("mul()")) for s in match.split(",")]
            sum += numbers[0] * numbers[1]
    print(sum)
