def parse(lines):
    wires = dict()
    gates = dict()
    for line in lines:
        words = line.strip().split()
        if '->' in line:
            input1 = words[0]
            op = words[1]
            input2 = words[2]
            output = words[4]
            gates[output] = ((input1, input2), op)
            for wire in [input1, input2, output]:
                if wire not in wires:
                    wires[wire] = None
        elif ':' in line:
            wire = words[0].strip(':')
            value = bool(int(words[1]))
            wires[wire] = value
    return wires, gates

def fill_wires(wire, wires, gates):
    if wire not in gates or wires[wire] != None:
        return
    gate = gates[wire]
    inputs = gate[0]
    op = gate[1]
    for input in inputs:
        fill_wires(input, wires, gates)
    input1 = wires[inputs[0]]
    input2 = wires[inputs[1]]
    if op == 'AND':
        wires[wire] = input1 and input2
    elif op == 'OR':
        wires[wire] = input1 or input2
    elif op == 'XOR':
        wires[wire] = input1 != input2

def z_decimal(wires, gates):
    z_wires = [wire for wire in wires if wire[0] == 'z']
    z_wires.sort()
    for wire in z_wires:
        fill_wires(wire, wires, gates)
    print([(wire, wires[wire]) for wire in z_wires])
    z_outputs = [wires[wire] for wire in z_wires]
    return to_decimal(z_outputs)

def to_decimal(bits: list[bool]) -> int:
    print(bits)
    return sum(bit * 2**i for i, bit in enumerate(bits))

with open('day24/input.txt', 'r') as f:
    lines = f.readlines()
    wires, gates = parse(lines)
    result = z_decimal(wires, gates)
    print(result)
