import re

use_example_input = False


def main():
    program = read_input()
    multi_sum = 0
    enabled = True
    while len(program) > 0:
        piece, program = get_next_piece(program, enabled)
        if enabled:
            multi_sum += sum(x * y for x, y in find_mul_instructions(piece))
        enabled = not enabled
    print(multi_sum)


def get_next_piece(program, enabled):
    switch_command = "don't()" if enabled else "do()"
    index = program.find(switch_command)
    piece = program[:index]
    program = program[index:] if index >= 0 else ""
    return piece, program


def find_mul_instructions(code):
    matches = re.findall(r"mul\((\d+),(\d+)\)", code)
    return [(int(x), int(y)) for x, y in matches]


def read_input():
    file_name = "example03.txt" if use_example_input else "input03.txt"
    with open(file_name, "r") as f:
        return f.read()


if __name__ == "__main__":
    main()
