use_example_input = False

BIT_COUNT = 3 if use_example_input else 45


class Adder:
    def __init__(self, inputs: dict, gates: dict):
        self.inputs = inputs
        self.gates = gates
        self.output_names = list(self.gates.keys())

    def calculate_output(self):
        output_value = 0
        for i in range(BIT_COUNT, -1, -1):
            output_name = get_wire_name("z", i)
            output_bit = 1 if self.get_value_on_wire(output_name) else 0
            output_value = output_value * 2 + output_bit
        return output_value

    def get_value_on_wire(self, wire_name):
        if wire_name in self.inputs:
            return self.inputs[wire_name]

        wire1, operand, wire2 = self.gates[wire_name]
        return bit_op(operand, self.get_value_on_wire(wire1), self.get_value_on_wire(wire2))

    def calculate(self, x, y):
        self.set_inputs("x", x)
        self.set_inputs("y", y)
        return self.calculate_output()

    def set_inputs(self, prefix, value):
        for i in range(BIT_COUNT):
            input_name = get_wire_name(prefix, i)
            bit = value & 1
            self.inputs[input_name] = bit
            value = value >> 1

    def swap_outputs_by_name(self, out1, out2):
        print(f"  Swapping {out1} <-> {out2}")
        gate1 = self.gates[out1]
        gate2 = self.gates[out2]
        self.gates[out1] = gate2
        self.gates[out2] = gate1

    def get_output_count(self):
        return len(self.output_names)

    def get_output_name(self, output_index):
        return self.output_names[output_index]

    def rename_initial_wires(self):
        c00_name = self.find_output_for("x00", "y00", "AND")
        self.rename_wire(c00_name, "c00")
        for i in range(1, BIT_COUNT):
            xor_gate_name = self.find_output_for(get_wire_name("x", i), get_wire_name("y", i), "XOR")
            if not xor_gate_name.startswith("z"):
                self.rename_wire(xor_gate_name, get_wire_name("xor", i))
            and_gate_name = self.find_output_for(get_wire_name("x", i), get_wire_name("y", i), "AND")
            if not and_gate_name.startswith("z"):
                self.rename_wire(and_gate_name, get_wire_name("and", i))

    def find_output_for(self, w1, w2, o) -> str:
        for output in self.gates:
            wire1, op, wire2 = self.gates[output]
            if op == o and ((wire1 == w1 and wire2 == w2) or (wire2 == w1 and wire1 == w2)):
                return output

    def rename_wire(self, original_name, new_name):
        self.gates[new_name] = self.gates.pop(original_name)
        for output in self.gates:
            wire1, op, wire2 = self.gates[output]
            if wire1 == original_name:
                self.gates[output] = (new_name, op, wire2)
            elif wire2 == original_name:
                self.gates[output] = (wire1, op, new_name)

    def check_and_rename_wires(self):
        for i in range(1, BIT_COUNT):
            c_prev_name = get_wire_name("c", i - 1)
            xor_name = get_wire_name("xor", i)
            z_name = get_wire_name("z", i)
            existing_z_name = self.find_output_for(c_prev_name, xor_name, "XOR")
            and_name = get_wire_name("and", i)
            if existing_z_name != z_name:
                if existing_z_name is None:
                    self.print_gates()
                    raise RuntimeError(f"Could not find Z{i}")
                self.swap_outputs_by_name(z_name, existing_z_name)
                x_name = get_wire_name("x", i)
                y_name = get_wire_name("y", i)
                if existing_z_name == self.find_output_for(x_name, y_name, "AND"):
                    print("    Setting proper name for the AND gate")
                    self.rename_wire(existing_z_name, and_name)
            d_wire_name = self.find_output_for(c_prev_name, xor_name, "AND")
            new_d_name = get_wire_name("d", i)
            self.rename_wire(d_wire_name, new_d_name)
            c_name = self.find_output_for(and_name, new_d_name, "OR")
            if c_name is None:
                self.print_gates()
                raise RuntimeError(f"Could not find gate C{i}")
            elif c_name != get_wire_name("z", i + 1):
                new_c_name = get_wire_name("c", i)
                self.rename_wire(c_name, new_c_name)

    def print_gates(self):
        outputs = sorted(list(self.gates.keys()))
        for output in outputs:
            wire1, op, wire2 = self.gates[output]
            print(f"{wire1} {op} {wire2} -> {output}")


def get_wire_name(prefix, i):
    padding = "0" if i < 10 else ""
    return prefix + padding + str(i)


def bit_op(operand: str, input1: int, input2: int):
    if operand == "AND":
        return input1 and input2
    elif operand == "OR":
        return input1 or input2
    elif operand == "XOR":
        return input1 ^ input2
    else:
        raise ValueError(f"Unknown operand: {operand}")
