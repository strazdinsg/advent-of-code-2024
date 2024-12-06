use_example_input = True

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

map = []
rows = 0
cols = 0
map = []

def main():
    global rows
    global cols
    global map
    read_input()
    rows = len(map)
    cols = len(map[0])
    pos = get_guard_position()
    while is_within_bounds(pos):
        mark_location(pos)
        pos = move(pos)
    visited = count_visited()
    print(visited)
    print_map()
    obstacles = count_loop_obstacles()
    print(obstacles)

def get_guard_position():
    global map
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '^':
                return (i, j, UP)

def is_within_bounds(pos):
    return pos[0] >= 0 and pos[0] < rows and pos[1] >= 0 and pos[1] < cols

def mark_location(pos):
    global map
    map[pos[0]] = map[pos[0]][:pos[1]] + str(pos[2]) + map[pos[0]][pos[1] + 1:]

def move(pos):
    next_pos = get_next_pos(pos)
    if is_wall(next_pos):
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

def is_wall(pos):
    global map
    return is_within_bounds(pos) and map[pos[0]][pos[1]] == '#'

def turn(pos):
    return (pos[0], pos[1], (pos[2] + 1) % 4)

def count_visited():
    global map
    visited = 0
    for row in map:
        for cell in row:
            if cell.isdigit():
                visited += 1
    return visited

def count_loop_obstacles():
    global rows
    global cols
    obstacles = 0
    for row in range(rows):
        for col in range(cols):
            # Try to place an obstacle on the left
            if is_dir((row, col, LEFT)) and gets_into_loop((row - 1, col, UP)):
                print(f"Putting obstacle at ({row}, {col-1})")
                obstacles += 1
            # Try to place an obstacle on the bottom
            if is_dir((row, col, DOWN)) and gets_into_loop((row, col - 1, LEFT)):
                print(f"Putting obstacle at ({row+1}, {col})")
                obstacles += 1
            # Try to place an obstacle on the right
            if is_dir((row, col, RIGHT)) and gets_into_loop((row + 1, col, DOWN)):
                print(f"Putting obstacle at ({row}, {col+1})")
                obstacles += 1
            # Try to place an obstacle on the top
            if is_dir((row, col, UP)) and gets_into_loop((row, col + 1, RIGHT)):
                print(f"Putting obstacle at ({row-1}, {col})")
                obstacles += 1
    return obstacles

def is_dir(pos):
    global map
    return map[pos[0]][pos[1]] == str(pos[2])

def gets_into_loop(pos):
    global map
    while is_within_bounds(pos):
        if is_dir(pos):
            return True
        pos = move(pos)
    return False

def read_input():
    global map
    file_name = "example06.txt" if use_example_input else "input06.txt"
    with open(file_name, "r") as f:
        map = f.read().splitlines()

def print_map():
    global map
    for row in map:
        print(row)

if __name__ == "__main__":
    main()


