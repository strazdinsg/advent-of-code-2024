use_example_input = False

START = 0
TOP = 9
UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

def main():
    map = read_input()
    # print_map(map)
    heads = find_heads(map)
    trail_count, top_count = find_trail_count(map, heads)
    print(top_count)
    print(trail_count)

def read_input():
    file_name = "example10.txt" if use_example_input else "input10.txt"
    with open(file_name, "r") as f:
        lines = f.read().splitlines()
        return [list(map(int, line)) for line in lines]

def find_heads(map):
    heads = []
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] == START:
                heads.append((row, col))
    return heads

def find_trail_count(map, heads):
    count = 0
    top_count = 0
    for head in heads:
        tops = set()
        count += count_trails(map, head, START, tops)
        top_count += len(tops)
    return count, top_count

def count_trails(map, pos, height, tops):
    if height == TOP:
        tops.add(pos)
        return 1
    neighbors = find_neighbors(map, pos)
    count = 0
    for neighbor in neighbors:
        count += count_trails(map, neighbor, height + 1, tops)
    return count

def find_neighbors(map, current):
    neighbors = []
    try_move(neighbors, map, current, UP)
    try_move(neighbors, map, current, RIGHT)
    try_move(neighbors, map, current, DOWN)
    try_move(neighbors, map, current, LEFT)
    return neighbors

def try_move(neighbors, map, current, dir):
    next = (current[0] + dir[0], current[1] + dir[1])
    current_height = map[current[0]][current[1]]
    if is_within_bounds(map, next) and map[next[0]][next[1]] == current_height + 1:
        neighbors.append(next)

def is_within_bounds(map, pos):
    return 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0])

def print_map(map):
    for line in map:
        print(line)

if __name__ == "__main__":
    main()
