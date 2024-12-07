use_example_input = False

def main():
    equations = read_input()
    normal_sum = calculate_calibration_sum(equations, False)
    print(normal_sum)
    concat_sum = calculate_calibration_sum(equations, True)
    print(concat_sum)

def read_input():
    file_name = "example07.txt" if use_example_input else "input07.txt"
    equations = []
    with open(file_name, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            if line == "":
                break
            result, operand_string = line.split(": ")
            result = int(result)
            operands = [int(operand) for operand in operand_string.split(" ")]
            equations.append({"res": result, "ops": operands})
    return equations

def calculate_calibration_sum(equations, allow_concat):
    s = 0
    for equation in equations:
        if can_be_true(equation, allow_concat):
            s += equation["res"]
    return s

def can_be_true(equation, allow_concat):
    return can_evaluate_to(equation, equation["ops"][0], 0, allow_concat)

def can_evaluate_to(equation, current_result, current_index, allow_concat):
    if current_index == len(equation["ops"]) - 1:
        return current_result == equation["res"]
    else:
        next_op = equation["ops"][current_index + 1]
        can = can_evaluate_to(equation, current_result + next_op, current_index + 1, allow_concat) \
            or can_evaluate_to(equation, current_result * next_op, current_index + 1, allow_concat)
        if not can and allow_concat:
            concatenated = int(str(current_result) + str(next_op))
            can = can_evaluate_to(equation, concatenated, current_index + 1, True)
        return can

if __name__ == "__main__":
    main()
