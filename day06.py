use_example_input = False

EMPTY = -1
WALL = -2

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

map = []
rows = 0
cols = 0

def main():
    global rows
    global cols
    map = read_input()
    # print_map(map)
    rows = len(map)
    cols = len(map[0])
    starting_map = copy_map(map)
    traverse_and_check_loop(map)
    visited = count_visited(map)
    print(visited)
    # print_map(map)
    obstacles = count_loop_obstacles(starting_map)
    print(obstacles)

def get_guard_position(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == UP:
                return (i, j, UP)

def copy_map(m):
    return [row[:] for row in m]

def traverse_and_check_loop(map):
    pos = get_guard_position(map)
    if pos is None:
        raise Exception("Guard not found")
    while is_within_bounds(map, pos):
        mark_location(map, pos)
        pos = move(map, pos)
        if (is_dir(map, pos)):
            return True
    return False

def is_within_bounds(map, pos):
    return pos[0] >= 0 and pos[0] < len(map) and pos[1] >= 0 and pos[1] < len(map[0])

def mark_location(map, pos):
    map[pos[0]][pos[1]] = pos[2]

def move(map, pos):
    next_pos = get_next_pos(pos)
    if is_wall(map, next_pos):
        return turn(pos)
    else:
        return next_pos

def get_next_pos(pos):
    if pos[2] == UP:
        return (pos[0] - 1, pos[1], UP)
    elif pos[2] == RIGHT:
        return (pos[0], pos[1] + 1, RIGHT)
    elif pos[2] == DOWN:
        return (pos[0] + 1, pos[1], DOWN)
    elif pos[2] == LEFT:
        return (pos[0], pos[1] - 1, LEFT)

def is_wall(map, pos):
    return is_within_bounds(map, pos) and map[pos[0]][pos[1]] == WALL

def turn(pos):
    return (pos[0], pos[1], (pos[2] + 1) % 4)

def count_visited(map):
    visited = 0
    for row in map:
        for cell in row:
            if cell != EMPTY and cell != WALL:
                visited += 1
    return visited

def count_loop_obstacles(map):
    obstacles = 0
    for row in range(len(map)):
        print(f"Checking obstacles for row {row}")
        for col in range(len(map[row])):
            if map[row][col] == EMPTY:
                map_copy = copy_map(map)
                map_copy[row][col] = WALL
                if traverse_and_check_loop(map_copy):
                    print(f"Could place obstacle at {row}, {col}")
                    obstacles += 1
    return obstacles

def is_dir(map, pos):
    return is_within_bounds(map, pos) and map[pos[0]][pos[1]] == pos[2]

def gets_into_loop(map, pos):
    while is_within_bounds(map, pos):
        if is_dir(map, pos):
            return True
        pos = move(map, pos)
    return False

def read_input():
    file_name = "example06.txt" if use_example_input else "input06.txt"
    with open(file_name, "r") as f:
        map = f.read().splitlines()
        return replace_strings_with_ints(map)

def replace_strings_with_ints(map):
    for i in range(len(map)):
        row = list(map[i])
        for j in range(len(row)):
            if row[j] == '.':
                row[j] = EMPTY
            elif row[j] == '^':
                row[j] = UP
            elif row[j] == '#':
                row[j] = WALL
        map[i] = row
    return map

def print_map(map):
    for row in map:
        print(row)

if __name__ == "__main__":
    main()


