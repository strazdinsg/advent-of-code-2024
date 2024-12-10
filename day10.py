use_example_input = False

START = 0
TOP = 9
UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)


def main():
    trail_map = read_input()
    # print_map(map)
    heads = find_heads(trail_map)
    trail_count, top_count = find_trail_count(trail_map, heads)
    print(top_count)
    print(trail_count)


def read_input():
    file_name = "example10.txt" if use_example_input else "input10.txt"
    with open(file_name, "r") as f:
        lines = f.read().splitlines()
        return [list(map(int, line)) for line in lines]


def find_heads(m):
    heads = []
    for row in range(len(m)):
        for col in range(len(m[0])):
            if m[row][col] == START:
                heads.append((row, col))
    return heads


def find_trail_count(m, heads):
    count = 0
    top_count = 0
    for head in heads:
        tops = set()
        count += count_trails(m, head, START, tops)
        top_count += len(tops)
    return count, top_count


def count_trails(m, pos, height, tops):
    if height == TOP:
        tops.add(pos)
        return 1
    neighbors = find_neighbors(m, pos)
    count = 0
    for neighbor in neighbors:
        count += count_trails(m, neighbor, height + 1, tops)
    return count


def find_neighbors(map, current):
    neighbors = []
    try_move(neighbors, map, current, UP)
    try_move(neighbors, map, current, RIGHT)
    try_move(neighbors, map, current, DOWN)
    try_move(neighbors, map, current, LEFT)
    return neighbors


def try_move(neighbors, m, current, direction):
    next_pos = (current[0] + direction[0], current[1] + direction[1])
    current_height = m[current[0]][current[1]]
    if is_within_bounds(m, next_pos) and m[next_pos[0]][next_pos[1]] == current_height + 1:
        neighbors.append(next_pos)


def is_within_bounds(m, pos):
    return 0 <= pos[0] < len(m) and 0 <= pos[1] < len(m[0])


def print_map(m):
    for line in m:
        print(line)


if __name__ == "__main__":
    main()
