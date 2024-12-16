use_example_input = False

START = "S"
END = "E"
WALL = "#"
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIRECTIONS = {
    UP: (-1, 0),
    RIGHT: (0, 1),
    DOWN: (1, 0),
    LEFT: (0, -1)
}
START_DIR = RIGHT
TURN_COST = 1000
MOVE_COST = 1
HDIR = ["UP", "RIGHT", "DOWN", "LEFT"]


def shortest_path_of(shortest_paths, pos):
    shortest = None
    for direction in DIRECTIONS:
        if (pos, direction) in shortest_paths:
            path_info = shortest_paths[(pos, direction)]
            distance, prev_positions = path_info
            if shortest is None or distance < shortest[0]:
                shortest = path_info
            elif distance == shortest[0]:
                shortest[1].append(pos)
    return shortest


def unwind_shortest_paths(shortest_paths, last_step):
    locations = set()
    to_visit = [last_step[1].pop()]
    while to_visit:
        position, direction = to_visit.pop()
        locations.add(position)
        shortest_distance, prev_positions = shortest_paths[(position, direction)]
        # print(f"Current: {position} [{HDIR[direction]}], shortest: {shortest_distance}")
        for prev_pos_and_dir in prev_positions:
            to_visit.append(prev_pos_and_dir)
    return locations


def get_previous_pos(current, direction):
    move = DIRECTIONS[direction]
    return current[0] - move[0], current[1] - move[1]


def main():
    input_file_name = "example16.txt" if use_example_input else "input16.txt"
    maze = read_input(input_file_name)
    start = find_in_maze(maze, START)
    end = find_in_maze(maze, END)
    print_maze(maze)
    shortest_paths = find_shortest_path(maze, start, end, START_DIR)
    last_step = shortest_path_of(shortest_paths, end)
    print(f"Shortest distance: {last_step[0]}")
    best_locations = unwind_shortest_paths(shortest_paths, last_step)
    print(f"Best location count: {len(best_locations) + 1}")


def find_in_maze(maze, char):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == char:
                return i, j
    return None


def find_shortest_path(maze, start, end, direction):
    to_visit = [(start, direction)]
    shortest = {(start, direction): (0, set())}
    while to_visit:
        current, direction = to_visit.pop()
        distance, prev_info = shortest[(current, direction)]
        # print(f"Current: {current}, direction: {direction}, distance: {distance}")
        # shortest[(current, direction)] = distance
        try_move(maze, current, direction, distance + MOVE_COST, shortest, to_visit)
        try_turn(current, (direction + 1) % 4, direction, distance + TURN_COST, shortest, to_visit)
        try_turn(current, (direction - 1) % 4, direction, distance + TURN_COST, shortest, to_visit)
    return shortest


def try_move(maze, current, direction, distance, shortest, to_visit):
    move = DIRECTIONS[direction]
    next_pos = (current[0] + move[0], current[1] + move[1])
    if not can_walk_to(maze, next_pos):
        return

    shortest_distance = get_shortest_distance_to(next_pos, shortest, direction)
    if shortest_distance is None or distance < shortest_distance:
        mark_new_best(shortest, current, next_pos, direction, direction, distance, to_visit)
    elif distance == shortest_distance:
        add_alternative_best(shortest, current, next_pos, direction, direction)


def try_turn(pos, direction, prev_dir, distance, shortest, to_visit):
    shortest_distance = get_shortest_distance_to(pos, shortest, direction)
    if shortest_distance is None or distance < shortest_distance:
        mark_new_best(shortest, pos, pos, direction, prev_dir, distance, to_visit)
    elif distance == shortest_distance:
        add_alternative_best(shortest, pos, pos, direction, prev_dir)


def mark_new_best(shortest, prev_pos, pos, direction, prev_dir, distance, to_visit):
    to_visit.append((pos, direction))
    shortest[(pos, direction)] = (distance, {(prev_pos, prev_dir)})


def add_alternative_best(shortest, prev_pos, pos, direction, prev_dir):
    d, prev_info = shortest[(pos, direction)]
    prev_info.add((prev_pos, prev_dir))


def can_walk_to(maze, pos):
    return is_within_bounds(maze, pos) and maze[pos[0]][pos[1]] != WALL


def is_within_bounds(maze, pos):
    return 0 <= pos[0] < len(maze) and 0 <= pos[1] < len(maze[0])


def get_shortest_distance_to(next_pos, shortest_distances, direction):
    if (next_pos, direction) not in shortest_distances:
        return None
    return shortest_distances[(next_pos, direction)][0]

# def is_better(next_pos, visited, direction, distance):
#     if (next_pos, direction) not in visited:
#         return True
#     return distance < visited[(next_pos, direction)][0]


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        return read_until_empty_line(f)


def read_until_empty_line(f):
    maze = []
    while True:
        line = f.readline().strip("\n")
        if line == "":
            break
        maze.append(line)
    return maze


def print_maze(maze):
    for line in maze:
        debug_print("".join(line))


DEBUG = True


def debug_print(*args):
    if DEBUG:
        print(*args)

if __name__ == "__main__":
    main()
