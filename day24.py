use_example_input = False


def main():
    input_file_name = "example24.txt" if use_example_input else "input24.txt"
    inputs, gates = read_input(input_file_name)
    output_gates = find_output_gates(gates)
    output_gate_names = get_desc_sorted_gate_names(output_gates)
    output_value = 0
    for output_name in output_gate_names:
        output_bit = 1 if get_value_on_wire(output_name, gates, inputs) else 0
        output_value = output_value * 2 + output_bit
    print(f"Part 1: {output_value}")


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        inputs = {}
        gates = {}
        input_lines = read_until_empty_line(f)
        for input_line in input_lines:
            signal_name, start_value = input_line.split(": ")
            inputs[signal_name] = int(start_value)
        gate_lines = read_until_empty_line(f)
        for gate_line in gate_lines:
            op, output_name = gate_line.split(" -> ")
            wire1, operation, wire2 = op.split(" ")
            gates[output_name] = (wire1, operation, wire2)
        return inputs, gates


def find_output_gates(gates):
    output_gates = {}
    for gate_name in gates:
        gate = gates[gate_name]
        if is_output_gate(gate_name):
            output_gates[gate_name] = gate
    return output_gates


def is_output_gate(gate_name: str):
    return gate_name.startswith("z")


def get_desc_sorted_gate_names(gates):
    return sorted(gates.keys(), reverse=True)


def get_value_on_wire(wire_name, gates, inputs):
    if wire_name in inputs:
        return inputs[wire_name]

    wire1, operand, wire2 = gates[wire_name]
    return bit_op(operand, get_value_on_wire(wire1, gates, inputs), get_value_on_wire(wire2, gates, inputs))


def bit_op(operand, input1, input2):
    if operand == "AND":
        return input1 and input2
    elif operand == "OR":
        return input1 or input2
    elif operand == "XOR":
        return input1 ^ input2
    else:
        raise ValueError(f"Unknown operand: {operand}")


def read_until_empty_line(f):
    lines = []
    while True:
        line = f.readline().strip("\n")
        if line == "":
            break
        lines.append(line)
    return lines


if __name__ == "__main__":
    main()
