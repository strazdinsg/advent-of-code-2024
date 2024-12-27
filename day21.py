from collections import deque

use_example_input = True

EMPTY = "."
APPROVE = "A"

NUMKEYS = "0123456789A"


def main():
    input_file_name = "example21.txt" if use_example_input else "input21.txt"
    codes = read_input(input_file_name)
    numpad, arrows = read_key_mappings("day21.dict")

    part(1, 2, numpad, arrows, codes)
    # part(2, 25, numpad, arrows, codes)


def part(nr, num_arrow_keypads, numpad, arrows, codes):
    command_chain = create_command_chain(num_arrow_keypads, numpad, arrows)
    chains = find_shortest_chains(command_chain)
    comp_sum = sum_complexities(chains, codes)
    print(f"Part {nr}: complexity sum = {comp_sum}")


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        codes = []
        line = f.readline().strip()
        while line != "":
            codes.append(line)
            line = f.readline().strip()
        return codes


def get_sequence(code, shortest_chains: dict[str, dict[str, str]], start_key):
    prev_key = start_key
    sequence = ""
    for i in range(len(code)):
        key = code[i]
        sequence += shortest_chains[prev_key][key]
        prev_key = key
    return sequence


def calculate_complexity(sequence, code):
    char_count = len(sequence)
    code_value = int(code[:-1])
    print(f"    {char_count}: {code_value}")
    return char_count * code_value


def find_shortest_chains(command_chain):
    global NUMKEYS
    shortest_chains = {}
    for from_key in NUMKEYS:
        shortest_chains[from_key] = {}
        print(f"    Generate chains for {from_key}")
        for to_key in NUMKEYS:
            c = get_shortest_chain(from_key, to_key, command_chain)
            shortest_chains[from_key][to_key] = c
    return shortest_chains


def get_shortest_chain(from_key, to_key, command_chain):
    numpad = command_chain[0]
    numpad_chains = numpad[from_key][to_key]
    all_chains = get_all_chains(numpad_chains, command_chain[1:])
    # Return item from all_chains with the shortest length
    shortest_chain = min(all_chains, key=len)
    return shortest_chain


def get_all_chains(prev_chains, command_chain):
    if len(command_chain) == 0:
        return prev_chains
    min_len = len(min(prev_chains, key=len))
    chains = []
    keypad = command_chain[0]
    to_visit = deque([])
    for pc in prev_chains:
        if len(pc) == min_len:
            to_visit.append((APPROVE + pc, ""))
    if len(prev_chains) > len(to_visit):
        print(f"Processing {len(to_visit)} from previous {len(prev_chains)} prev chains")
    while to_visit:
        prev_chain, processed = to_visit.popleft()
        prev_char = prev_chain[0]
        char = prev_chain[1]
        possible_chains = keypad[prev_char][char]
        if len(prev_chain) == 2:
            for chain in possible_chains:
                chains.append(processed + chain)
        else:
            for chain in possible_chains:
                to_visit.append((prev_chain[1:], processed + chain))
    return get_all_chains(chains, command_chain[1:])


def read_key_mappings(filename):
    with open(filename, "r") as f:
        numpad = read_key_mapping(f)
        arrows = read_key_mapping(f)
        return numpad, arrows


def read_key_mapping(f):
    line = f.readline().strip()
    mapping = {}
    while line != "":
        change, sequence_list = line.split(":")
        from_key, to_key = change.split("-")
        sequences = sequence_list.split(",")
        if from_key not in mapping:
            mapping[from_key] = {}
        mapping[from_key][to_key] = sequences
        line = f.readline().strip()
    return mapping


def create_command_chain(num_arrow_keypads, numpad, arrows):
    command_chain = [numpad]
    for i in range(num_arrow_keypads):
        command_chain.append(arrows)
    return command_chain


def sum_complexities(chains, codes):
    comp_sum = 0
    for code in codes:
        s = get_sequence(code, chains, "A")
        print(f"{code}: [{len(s)}] {s}")
        comp_sum += calculate_complexity(s, code)
    return comp_sum


if __name__ == "__main__":
    main()