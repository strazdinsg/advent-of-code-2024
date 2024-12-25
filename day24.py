use_example_input = False


class Adder:
    def __init__(self, inputs, gates):
        self.inputs = inputs
        self.gates = gates
        self.output_gates = self._find_output_gates()
        self.output_gate_names = self.get_desc_sorted_gate_names()

    def _find_output_gates(self):
        output_gates = {}
        for gate_name in self.gates:
            gate = self.gates[gate_name]
            if self.is_output_gate(gate_name):
                output_gates[gate_name] = gate
        return output_gates

    @staticmethod
    def is_output_gate(gate_name: str):
        return gate_name.startswith("z")

    def get_desc_sorted_gate_names(self):
        return sorted(self.output_gates.keys(), reverse=True)

    def calculate_output(self):
        output_value = 0
        for output_name in self.output_gate_names:
            output_bit = 1 if self.get_value_on_wire(output_name) else 0
            output_value = output_value * 2 + output_bit
        return output_value

    def get_value_on_wire(self, wire_name):
        if wire_name in self.inputs:
            return self.inputs[wire_name]

        wire1, operand, wire2 = self.gates[wire_name]
        return self.bit_op(operand, self.get_value_on_wire(wire1), self.get_value_on_wire(wire2))

    @staticmethod
    def bit_op(operand, input1, input2):
        if operand == "AND":
            return input1 and input2
        elif operand == "OR":
            return input1 or input2
        elif operand == "XOR":
            return input1 ^ input2
        else:
            raise ValueError(f"Unknown operand: {operand}")


def main():
    input_file_name = "example24.txt" if use_example_input else "input24.txt"
    inputs, gates = read_input(input_file_name)
    adder = Adder(inputs, gates)
    part1(adder)
    part2(adder)


def part1(adder):
    print(f"Part 1: {adder.calculate_output()}")


def part2(adder):
    pass


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
