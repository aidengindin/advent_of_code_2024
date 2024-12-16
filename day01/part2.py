with open("day1/input.txt") as f:
    lines = f.readlines()
    left = [int(line.split()[0]) for line in lines]
    right = [int(line.split()[1]) for line in lines]
    left.sort()
    right.sort()
    similarity = sum([x * right.count(x) for x in left])
    print(similarity)
