use_example_input = False

MAX_HEIGHT = 5


def main():
    input_file_name = "example25.txt" if use_example_input else "input25.txt"
    locks, keys = read_input(input_file_name)
    possible_fits = 0
    for lock in locks:
        for key in keys:
            possible_fits += 1 if is_fit(key, lock) else 0
    print(f"Part 1: {possible_fits}")


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        locks = []
        keys = []
        pattern = read_until_empty_line(f)
        while pattern:
            if pattern[0] == "#####":
                locks.append(parse_lock(pattern))
            else:
                keys.append(parse_key(pattern))
            pattern = read_until_empty_line(f)
        return locks, keys


def parse_lock(pattern):
    lock = [0, 0, 0, 0, 0]
    for position in range(5):
        lock[position] = find_lock_height(pattern, position)
    return lock


def find_lock_height(pattern, position):
    for h in range(len(pattern) - 1, -1, -1):
        if pattern[h][position] == "#":
            return h
    return None


def parse_key(pattern):
    key = [0, 0, 0, 0, 0]
    for position in range(5):
        key[position] = find_key_height(pattern, position)
    return key


def find_key_height(pattern, position):
    pattern_height = len(pattern) - 1
    for h in range(len(pattern)):
        if pattern[h][position] == "#":
            return pattern_height - h
    return None


def read_until_empty_line(f):
    lines = []
    while True:
        line = f.readline().strip("\n")
        if line == "":
            break
        lines.append(line)
    return lines


def is_fit(key, lock):
    for i in range(len(key)):
        if key[i] + lock[i] > MAX_HEIGHT:
            return False
    return True

if __name__ == "__main__":
    main()
