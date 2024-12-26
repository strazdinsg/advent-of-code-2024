from adder import use_example_input, Adder, BIT_COUNT


def main():
    input_file_name = "example24.txt" if use_example_input else "input24.txt"
    inputs, gates = read_input(input_file_name)
    adder = Adder(inputs, gates)
    print(f"Part 1: {adder.calculate_output()}")

    print("Bit errors in the start:")
    print_bit_errors(adder)

    print("Fixing wires...")
    # These two I found manually
    adder.swap_outputs_by_name("pvb", "qdq")

    adder.rename_initial_wires()
    adder.check_and_rename_wires()

    # This allows to look at the graph manually. Paste the Mermaid syntax into an MD file
    # adder.print_graph_in_mermaid_syntax()

    print("Bit errors after swaps:")
    print_bit_errors(adder)


def print_bit_errors(adder):
    for bit_nr in range(BIT_COUNT):
        n = 1 << bit_nr
        r1 = adder.calculate(n, 0)
        r2 = adder.calculate(0, n)
        r3 = adder.calculate(n, n)
        if r1 != n or r2 != n or r3 != 2 * n:
            print(f"  Fail in bit {bit_nr}")


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
