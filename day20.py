from collections import deque

use_example_input = False

START = "S"
END = "E"
EMPTY = "."
WALL = "#"
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
MIN_CHEAT_SAVING = 20 if use_example_input else 100


def main():
    input_file_name = "example20.txt" if use_example_input else "input20.txt"
    maze = read_input(input_file_name)
    start_pos = find_position(maze, START)
    end_pos = find_position(maze, END)
    find_shortest_paths(maze, start_pos, end_pos)
    print(f"Part 1: {count_cheats(maze, MIN_CHEAT_SAVING, 2)}")
    print(f"Part 2: {count_cheats(maze, MIN_CHEAT_SAVING, 20)}")


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        maze = []
        line = f.readline().strip()
        while line != "":
            maze.append([c for c in line])
            line = f.readline().strip()
        return maze


def find_position(maze, char):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == char:
                return row, col
    return None, None


def find_shortest_paths(maze, start_pos, end_pos):
    to_visit = deque([(start_pos, 0)])
    maze[start_pos[0]][start_pos[1]] = 0
    while to_visit:
        current, distance = to_visit.popleft()
        for d in DIRECTIONS:
            new_pos = move(current, d)
            if is_empty(maze, new_pos):
                to_visit.append((new_pos, distance + 1))
                maze[new_pos[0]][new_pos[1]] = distance + 1


def move(pos, d):
    return pos[0] + d[0], pos[1] + d[1]


def is_empty(maze, pos):
    return is_within_bounds(maze, pos) and \
        (maze[pos[0]][pos[1]] == EMPTY or maze[pos[0]][pos[1]] == END)


def is_within_bounds(maze, pos):
    return 0 <= pos[0] < len(maze) and 0 <= pos[1] < len(maze[0])


def count_cheats(maze, min_saving, max_cheat_length):
    cheat_count = 0
    for row in range(1, len(maze)):
        for col in range(1, len(maze[0])):
            cheat_count += try_cheat(maze, (row, col), min_saving, max_cheat_length)
    return cheat_count


def try_cheat(maze, pos, min_saving, max_cheat_length):
    distance = get_distance_at(maze, pos)
    if distance is None:
        return 0
    cheat_count = 0
    for dr in range(-max_cheat_length, max_cheat_length + 1):
        for dc in range(-max_cheat_length, max_cheat_length + 1):
            cheat_length = abs(dr) + abs(dc)
            if cheat_length <= max_cheat_length:
                next_pos = move(pos, (dr, dc))
                next_distance = get_distance_at(maze, next_pos)
                if next_distance is not None and next_distance > distance:
                    cheat_saving = next_distance - distance - cheat_length
                    if cheat_saving >= min_saving:
                        cheat_count += 1
    return cheat_count


def is_wall(maze, pos):
    return is_within_bounds(maze, pos) and maze[pos[0]][pos[1]] == WALL


def get_distance_at(maze, pos):
    if not is_within_bounds(maze, pos):
        return None
    m = maze[pos[0]][pos[1]]
    return m if isinstance(m, int) else None


if __name__ == "__main__":
    main()

