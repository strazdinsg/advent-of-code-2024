use_example_input = False

num_ways = {}


def main():
    input_file_name = "example19.txt" if use_example_input else "input19.txt"
    towels, designs = read_input(input_file_name)
    num_doable = 0
    doable_ways = 0
    for design in designs:
        ways = get_num_ways(design, towels)
        if ways > 0:
            num_doable += 1
            doable_ways += ways
    print(f"Number of doable designs: {num_doable}")
    print(f"Number of ways to doable designs: {doable_ways}")


def get_num_ways(design: str, towels: list[str]):
    global num_ways
    if design in num_ways:
        return num_ways[design]
    ways = 0
    for towel in towels:
        if design == towel:
            ways += 1
        elif design.startswith(towel):
            ways += get_num_ways(design[len(towel):], towels)
    num_ways[design] = ways
    return ways


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        towels = f.readline().strip().split(", ")
        f.readline()
        designs = []
        while True:
            pattern = f.readline().strip()
            if pattern != "":
                designs.append(pattern)
            else:
                break
        return towels, designs


if __name__ == "__main__":
    main()
