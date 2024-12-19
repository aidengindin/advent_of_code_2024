register_a = 0
register_b = 0
register_c = 0
output = ""

def parse(lines):
    global register_a, register_b, register_c
    register_a = int(lines[0].split()[2])
    register_b = int(lines[1].split()[2])
    register_c = int(lines[2].split()[2])
    instructions_string = lines[4].split()[1].split(",")
    instructions = []
    for i in range(0, len(instructions_string), 2):
        instruction = int(instructions_string[i])
        operand = int(instructions_string[i+1])
        instructions.append((instruction, operand))
    return instructions

def read_combo(operand):
    global register_a, register_b, register_c
    if operand < 4:
        return operand
    if operand == 4:
        return register_a
    if operand == 5:
        return register_b
    if operand == 6:
        return register_c

def run(program):
    pointer = 0
    while pointer < len(program):
        # print("pointer:", pointer)
        # print("register_a:", register_a)
        # print("register_b:", register_b)
        # print("register_c:", register_c)
        pair = program[pointer]
        opcode = pair[0]
        operand = pair[1]
        # print("opcode:", opcode)
        # print("operand:", operand)
        # print()
        pointer = execute(opcode, operand, pointer)
    # print("pointer:", pointer)

def execute(opcode, operand, pointer):
    global register_a, register_b, register_c, output
    if opcode == 0:  # adv
        register_a = int(register_a / (2 ** read_combo(operand)))
    elif opcode == 1:  # bxl
        register_b = register_b ^ operand
    elif opcode == 2:  # bst
        register_b = read_combo(operand) % 8
    elif opcode == 3:  # jnz
        if register_a > 0:
            return int(operand / 2)
    elif opcode == 4:  # bxc
        register_b = register_b ^ register_c
    elif opcode == 5:  # out
        result = str(read_combo(operand) % 8)
        if len(output) == 0:
            output += result
        else:
            output += "," + result
    elif opcode == 6:  # bdv
        register_b = int(register_a / (2 ** read_combo(operand)))
    elif opcode == 7:  # cdv:
        register_c = int(register_a / (2 ** read_combo(operand)))
    return pointer + 1

with open("day17/test2.txt", "r") as f:
    lines = f.readlines()
    program = parse(lines)
    run(program)
    print(output)