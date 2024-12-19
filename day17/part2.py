"""
Simplifying assumptions:

1. The program's last instruction is always 3,0
2. The program has exactly one adv instruction
3. The program has exactly one out instruction
4. Registers b and c are reset on every program iteration (they do not depend on their values in prior iterations)
"""

def parse(lines):
    return [int(octal) for octal in lines[4].split()[1].split(",")]

def read_combo(operand, register_a, register_b, register_c):
    if operand < 4:
        return operand
    if operand == 4:
        return register_a
    if operand == 5:
        return register_b
    if operand == 6:
        return register_c

def execute(opcode, operand, register_a, register_b, register_c, out):
    if opcode == 0:  # adv
        register_a = int(register_a / (2 ** read_combo(operand, register_a, register_b, register_c)))
    elif opcode == 1:  # bxl
        register_b = register_b ^ operand
    elif opcode == 2:  # bst
        register_b = read_combo(operand, register_a, register_b, register_c) % 8
    elif opcode == 3:  # jnz
        pass  # we don't actually need to handle this
    elif opcode == 4:  # bxc
        register_b = register_b ^ register_c
    elif opcode == 5:  # out
        out = read_combo(operand, register_a, register_b, register_c) % 8
    elif opcode == 6:  # bdv
        register_b = int(register_a / (2 ** read_combo(operand, register_a, register_b, register_c)))
    elif opcode == 7:  # cdv:
        register_c = int(register_a / (2 ** read_combo(operand, register_a, register_b, register_c)))
    return register_a, register_b, register_c, out

def search(register_a_so_far, program, remaining_program):
    if len(remaining_program) == 0:
        return octals_to_int(register_a_so_far)
    current_target = remaining_program[-1]
    next_remaining_program = remaining_program[:-1]
    for potential_octal in range(8):
        register_a = octals_to_int(register_a_so_far + [potential_octal])
        register_b = 0
        register_c = 0
        out = None
        for i in range(0, len(program), 2):
            opcode = program[i]
            operand = program[i + 1]
            register_a, register_b, register_c, out = execute(opcode, operand, register_a, register_b, register_c, out)
        if out == current_target:
            result = search(register_a_so_far + [potential_octal], program, next_remaining_program)
            if result:
                return result
    return None
    
def octals_to_int(octals):
    return sum(digit * 8**i for i, digit in enumerate(octals[::-1]))

with open("day17/input.txt", "r") as f:
    lines = f.readlines()
    program = parse(lines)
    register_a = search([], program, program)
    print(register_a)
