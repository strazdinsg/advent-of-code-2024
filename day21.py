use_example_input = False

EMPTY = "."
APPROVE = "A"

NUMPAD = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    APPROVE: (3, 2),
    EMPTY: (3, 0),
}

ARROWS = {
    EMPTY: (0, 0),
    "^": (0, 1),
    APPROVE: (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


class KeyPad:
    def __init__(self, keypad):
        self.keypad = keypad
        self.empty_pos = self.keypad[EMPTY]
        self.key_map = self.find_shortest()

    def find_shortest(self):
        key_map = {}
        for from_key in self.keypad:
            if from_key == EMPTY:
                continue
            key_map[from_key] = {}
            for to_key in self.keypad:
                if to_key == EMPTY:
                    continue
                if from_key != to_key:
                    key_map[from_key][to_key] = self.find_shortest_path(from_key, to_key)
                else:
                    key_map[from_key][to_key] = ""
        return key_map

    def find_shortest_path(self, from_key, to_key):
        from_pos = self.keypad[from_key]
        to_pos = self.keypad[to_key]
        dy = to_pos[0] - from_pos[0]
        dx = to_pos[1] - from_pos[1]
        dxs = ">" if dx > 0 else "<"
        dys = "v" if dy > 0 else "^"
        vdx = dxs * abs(dx)
        vdy = dys * abs(dy)
        if self.empty_pos[0] == from_pos[0]:
            return vdy + vdx
        else:
            return vdx + vdy

    def get_shortest(self, from_key, to_key):
        return self.key_map[from_key][to_key]


def main():
    input_file_name = "example21.txt" if use_example_input else "input21.txt"
    codes = read_input(input_file_name)
    numpad_map = KeyPad(NUMPAD)
    arrow_map = KeyPad(ARROWS)
    command_chain = [numpad_map, arrow_map, arrow_map]
    comp_sum = 0
    for code in codes:
        print(f"{code}:")
        s = get_multi_step_sequence(code, command_chain, "A")
        comp_sum += calculate_complexity(s, code)
    print(f"Complexity sum: {comp_sum}")


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        codes = []
        line = f.readline().strip()
        while line != "":
            codes.append(line)
            line = f.readline().strip()
        return codes


def get_multi_step_sequence(code, command_chain, start_key):
    sequence = code
    for keypad in command_chain:
        sequence = get_sequence(sequence, keypad, start_key)
        print(f"    {sequence}")
    return sequence


def get_sequence(code, keypad, start_key):
    code = code
    prev_key = start_key
    sequence = ""
    for i in range(len(code)):
        key = code[i]
        sequence += keypad.get_shortest(prev_key, key)
        sequence += APPROVE
        prev_key = key
    return sequence


def calculate_complexity(sequence, code):
    char_count = len(sequence)
    code_value = int(code[:-1])
    print(f"    {char_count}: {code_value}")
    return char_count * code_value


if __name__ == "__main__":
    main()