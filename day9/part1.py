def parse(line):
    line = line.strip()
    filesystem = []
    num_files = 0
    for i in range(len(line)):
        count = int(line[i])
        if i % 2 == 0:
            filesystem += [num_files] * count
            num_files += 1
        else:
            filesystem += [None] * count
    return filesystem

def compact(filesystem):
    empty_pointer = 0
    block_pointer = len(filesystem) - 1
    while block_pointer > empty_pointer:
        if filesystem[block_pointer] == None:
            block_pointer -= 1
            continue
        if filesystem[empty_pointer] != None:
            empty_pointer += 1
            continue
        block = filesystem[block_pointer]
        filesystem[empty_pointer] = block
        filesystem[block_pointer] = None
        empty_pointer += 1
        block_pointer -= 1
    return filesystem

def checksum(filesystem):
    return sum([(index * file_id if file_id != None else 0) for index, file_id in enumerate(filesystem)])

with open("day9/input.txt", "r") as f:
    line = f.readlines()[0]
    filesystem = parse(line)
    filesystem = compact(filesystem)
    check = checksum(filesystem)
    print(check)
