from collections import deque

use_example_input = False

MAZE_SIZE = 7 if use_example_input else 71
EMPTY = "."
CORRUPTED = "#"
TIME_LIMIT_PART_1 = 12 if use_example_input else 1024
TARGET = (MAZE_SIZE - 1, MAZE_SIZE - 1)


def main():
    input_file_name = "example18.txt" if use_example_input else "input18.txt"
    corrupted = read_input(input_file_name)

    shortest = try_find_path(corrupted, TIME_LIMIT_PART_1)
    print(f"Part 1. Shortest path: {shortest}")

    c = 0
    shortest = -1
    while shortest is not None:
        c += 1
        shortest = try_find_path(corrupted, c)
    print(f"Part 2. No path after corrupting {corrupted[c-1][0]},{corrupted[c-1][1]}")


def create_maze(corrupted, time_limit):
    maze = [[EMPTY for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
    for i in range(time_limit):
        col, row = corrupted[i]
        maze[row][col] = CORRUPTED
    return maze


def try_find_path(corrupted, time_limit):
    maze = create_maze(corrupted, time_limit)
    return find_shortest_path(maze)


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        lines = f.readlines()
        return [tuple(map(int, line.strip().split(","))) for line in lines]


def find_shortest_path(maze):
    to_visit = deque([(0, 0, 0)])
    visited = {}
    while to_visit:
        row, col, dist = to_visit.popleft()
        if (row, col) == TARGET:
            return dist
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            new_row = row + dr
            new_col = col + dc
            if 0 <= new_row < MAZE_SIZE and 0 <= new_col < MAZE_SIZE:
                if (new_row, new_col) not in visited and maze[new_row][new_col] == EMPTY:
                    to_visit.append((new_row, new_col, dist + 1))
                    visited[(new_row, new_col)] = dist + 1
    return None


def print_maze(maze):
    for y in range(MAZE_SIZE):
        print("".join(str(cell) for cell in maze[y]))


if __name__ == "__main__":
    main()
