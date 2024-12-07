use_example_input = False

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
WALL = 8

def main():
    map = read_input()
    starting_map = copy_map(map)
    traverse_and_check_loop(map)
    print("Note - calculation for Part 2 will take some time!")
    visited = count_visited(map)
    print("Answer for Part 1:", visited)
    obstacle_count = try_place_obstacles(starting_map)
    print("Answer for Part 2:", obstacle_count)

def get_guard_position(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if contains_direction(map, (i, j, UP)):
                return (i, j, UP)

def copy_map(original_m):
    new_m = []
    for row in original_m:
        r = []
        for cell in row:
            r.append(cell.copy())
        new_m.append(r)
    return new_m

def traverse_and_check_loop(map):
    pos = get_guard_position(map)
    if pos is None:
        raise Exception("Guard not found")
    map[pos[0]][pos[1]] = set() # Clear guard position, because it will be marked again
    while is_within_bounds(map, pos):
        mark_location(map, pos)
        pos = move(map, pos)
        if (contains_direction(map, pos)):
            return True
    return False

def is_within_bounds(map, pos):
    return 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0])

def mark_location(map, pos):
    row = pos[0]
    col = pos[1]
    dir = pos[2]    
    if WALL in map[row][col]:
        raise Exception("Can't walk into wall!")
    if dir in map[row][col]:
        print_map(map)
        print(pos)
        raise Exception("Loop should have been detected - can't walk the same cell in the same direction!")
    map[row][col].add(dir)

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
    return is_within_bounds(map, pos) and WALL in map[pos[0]][pos[1]]

def turn(pos):
    return (pos[0], pos[1], (pos[2] + 1) % 4)

def count_visited(map):
    visited = 0
    for row in map:
        for cell in row:
            if UP in cell or RIGHT in cell or DOWN in cell or LEFT in cell:
                visited += 1
    return visited

def try_place_obstacles(map):
    obstacles = 0
    inc = 100 / len(map)
    perc = 0
    for row in range(len(map)):
        print(f"Checking obstacles for row {row}, {int(perc)}% done")
        for col in range(len(map[row])):
            if not WALL in map[row][col] and not UP in map[row][col]:
                map_copy = copy_map(map)
                map_copy[row][col] = {WALL}
                if traverse_and_check_loop(map_copy):
                    obstacles += 1
        perc += inc
    return obstacles

def contains_direction(map, pos):
    return is_within_bounds(map, pos) and pos[2] in map[pos[0]][pos[1]]

def read_input():
    file_name = "example06.txt" if use_example_input else "input06.txt"
    with open(file_name, "r") as f:
        map = f.read().splitlines()
        return replace_strings_with_sets(map)

def replace_strings_with_sets(map):
    for i in range(len(map)):
        row = list(map[i])
        for j in range(len(row)):
            if row[j] == '.':
                row[j] = set()
            elif row[j] == '^':
                row[j] = {UP}
            elif row[j] == '#':
                row[j] = {WALL}
        map[i] = row
    return map

def print_map(map):
    for row in map:
        line = ""
        for cell in row:
            line += set_to_debug_char(cell)
        print(line)

def set_to_debug_char(s):
    if WALL in s:
        return "#"
    elif not s:
        return "."
    elif (UP in s or DOWN in s) and (LEFT in s or RIGHT in s):
        return "+"
    elif UP in s and DOWN in s:
        return "|"
    elif LEFT in s and RIGHT in s:
        return "-"
    elif UP in s:
        return "^"
    elif DOWN in s:
        return "v"
    elif LEFT in s:
        return "<"
    elif RIGHT in s:
        return ">"
    else:
        raise("Invalid map cell: " + str(s))
    

if __name__ == "__main__":
    main()
