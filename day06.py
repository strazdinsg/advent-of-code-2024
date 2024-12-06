use_example_input = False

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
    while guard_within_bounds(pos):
        mark_location(pos)
        pos = move(pos)
    visited = count_visited()
    print(visited)
    # print_map()
    obstacles = count_loop_obstacles()
    print(obstacles)

def get_guard_position():
    global map
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '^':
                return (i, j, UP)

def guard_within_bounds(pos):
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
    return guard_within_bounds(pos) and map[pos[0]][pos[1]] == '#'

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
            if is_dir(row, col, LEFT) and row >= 2 and col >= 1:
                if is_dir(row - 1, col, UP) or (is_dir(row - 1, col, RIGHT) and is_wall((row - 2, col, RIGHT)) or (is_dir(row - 2, col, UP))):
                    # print(f"Putting obstacle at ({row}, {col-1})")
                    obstacles += 1
            # Try to place an obstacle on the bottom
            if is_dir(row, col, DOWN) and row < rows - 1 and col >= 2:
                if is_dir(row, col - 1, LEFT) or (is_dir(row, col - 1, UP) and is_wall((row, col - 2, UP)) or (is_dir(row, col - 2, LEFT))):
                    # print(f"Putting obstacle at ({row+1}, {col})")
                    obstacles += 1
            # Try to place an obstacle on the right
            if is_dir(row, col, RIGHT) and row < rows - 2 and col < cols - 1:
                if is_dir(row + 1, col, DOWN) or (is_dir(row + 1, col, LEFT) and is_wall((row + 2, col, LEFT)) or (is_dir(row + 2, col, DOWN))):
                    # print(f"Putting obstacle at ({row}, {col+1})")
                    obstacles += 1
            # Try to place an obstacle on the top
            if is_dir(row, col, UP) and row >= 1 and col < cols - 2:
                if is_dir(row, col + 1, RIGHT) or (is_dir(row, col + 1, DOWN) and is_wall((row, col + 2, DOWN)) or (is_dir(row, col + 2, RIGHT))):
                    # print(f"Putting obstacle at ({row-1}, {col})")
                    obstacles += 1
    return obstacles

def is_dir(row, col, direction):
    global map
    return map[row][col] == str(direction)

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


