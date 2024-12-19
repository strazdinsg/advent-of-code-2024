import re

use_example_input = False

ADV = 0
BXL = 1
BST = 2
JNZ = 3
BXC = 4
OUT = 5
BDV = 6
CDV = 7


class Computer:
    def __init__(self, rega, regb, regc, instructions):
        self.rega = rega
        self.regb = regb
        self.regc = regc
        self.instructions = instructions
        self.output = []
        self.pc = 0
        self.valid = True

    def __str__(self):
        return f"[{self.rega}, {self.regb}, {self.regc}, {self.pc}]"

    def execute(self, try_reproduce):
        while 0 <= self.pc < len(self.instructions):
            self.execute_one_instruction()
            self.pc += 2
            if try_reproduce and not self.is_valid():
                break

    def is_valid(self):
        return self.valid and len(self.output) < len(self.instructions)

    def execute_one_instruction(self):
        instruction = self.instructions[self.pc]
        operand = self.instructions[self.pc + 1]
        if instruction == ADV:
            self.rega = self.rega // 2 ** self.get_combo(operand)
        elif instruction == BXL:
            self.regb = self.regb ^ operand
        elif instruction == BST:
            self.regb = self.get_combo(operand) % 8
        elif instruction == JNZ:
            if self.rega != 0:
                self.pc = operand - 2
        elif instruction == BXC:
            self.regb = self.regb ^ self.regc
        elif instruction == OUT:
            o = self.get_combo(operand) % 8
            self.output.append(o)
            index = len(self.output) - 1
            if o != self.instructions[index]:
                self.valid = False
        elif instruction == BDV:
            self.regb = self.rega // 2 ** self.get_combo(operand)
        elif instruction == CDV:
            self.regc = self.rega // 2 ** self.get_combo(operand)
        else:
            raise Exception(f"Invalid instruction: {instruction}")

    def get_combo(self, combo_op):
        if combo_op <= 3:
            return combo_op
        elif combo_op == 4:
            return self.rega
        elif combo_op == 5:
            return self.regb
        elif combo_op == 6:
            return self.regc
        else:
            raise Exception(f"Invalid combo op: {combo_op}")


def main():
    input_file_name = "example17.txt" if use_example_input else "input17.txt"
    rega, regb, regc, instructions = read_input(input_file_name)
    print(f"Reg A: {rega}, Reg B: {regb}, Reg C: {regc}")
    print(f"Instructions: {instructions}")
    # Part 1
    computer = Computer(rega, regb, regc, instructions)
    computer.execute(False)
    print(f"Output: {computer.output}")

    # Part 2
    to_visit = [(0, 1)]
    min_match = None
    while to_visit:
        reg_a, instr_count = to_visit.pop()
        instr_to_match = instructions[-instr_count:]
        matching = find_reg_a_matching(instructions, instr_to_match, reg_a)
        if instr_count == len(instructions) and len(matching) > 0:
            match = matching[0]
            if min_match is None or match < min_match:
                min_match = match
        else:
            for reg_a_match in matching:
                to_visit.append((reg_a_match * 8, instr_count + 1))
    print(f"Min match (Part 2): {min_match}")


def find_reg_a_matching(instructions, instr_subset, starting_reg_a):
    matching = []
    for reg_a in range(starting_reg_a, starting_reg_a + 8):
        computer = Computer(reg_a, 0, 0, instructions)
        computer.execute(False)
        if computer.output == instr_subset:
            matching.append(reg_a)
    return matching


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        rega = int(re.findall(r"Register A: (\d+)", f.readline())[0])
        regb = int(re.findall(r"Register B: (\d+)", f.readline())[0])
        regc = int(re.findall(r"Register C: (\d+)", f.readline())[0])
        f.readline()
        instr_string = re.findall("Program: (.+)", f.read())[0]
        instructions = [int(instr) for instr in instr_string.split(",")]
        return rega, regb, regc, instructions


if __name__ == "__main__":
    main()
