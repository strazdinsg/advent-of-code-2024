import copy

use_example_input = False


def main():
    input_file_name = "example15.txt" if use_example_input else "input15.txt"
    maze, commands = read_input(input_file_name)
    maze_copy = copy.deepcopy(maze)
    do_movements(maze, commands, False)
    do_movements(maze_copy, commands, True)


def do_movements(maze, commands, do_expand):
    if do_expand:
        maze = expand_horizontally(maze)
    robot = find_robot(maze)
    debug_print(f"Robot at {robot}")
    print_maze(maze)
    for command in commands:
        robot = move_one_step(maze, command, robot)
        # print_maze(maze)
    print("GPS positions:", get_gps_positions(maze))


def expand_horizontally(maze):
    new_maze = []
    replacements = {
        BOX: BOX_LEFT + BOX_RIGHT,
        WALL: WALL + WALL,
        EMPTY: EMPTY + EMPTY,
        ROBOT: ROBOT + EMPTY
    }
    for line in maze:
        new_line = []
        for char in line:
            if char in replacements:
                cc = replacements[char]
                new_line.append(cc[0])
                new_line.append(cc[1])
                continue
            else:
                raise Exception("Unexpected char: " + char)
        new_maze.append(new_line)
    return new_maze


def find_robot(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == ROBOT:
                return i, j
    return None


class Range:
    def __init__(self, start_x: int, end_x: int, y: int):
        self.y = y
        self.start_x = start_x
        self.end_x = end_x

    def __str__(self):
        return f"({self.start_x}-{self.end_x}, {self.y})"

    def extend(self, other):
        if self.y == other.y:
            self.start_x = min(self.start_x, other.start_x)
            self.end_x = max(self.end_x, other.end_x)
        else:
            raise Exception("Cannot extend range to different y")

    def in_direction(self, direction):
        return Range(self.start_x, self.end_x, self.y + direction)


def move_one_step(maze, command, robot):
    debug_print(command, robot)
    move = DIR[command]
    next_pos = get_next_pos(robot, move)
    if maze[next_pos[0]][next_pos[1]] == WALL:
        debug_print("  Wall")
        return robot
    elif maze[next_pos[0]][next_pos[1]] == EMPTY:
        debug_print("  Empty, moving")
        return move_robot(maze, robot, next_pos)
    elif is_box(maze, next_pos):
        debug_print("  Box")
        if is_horizontal(move):
            empty = find_first_empty(maze, next_pos, move)
            if empty is not None:
                debug_print("    Horizontal move to", empty)
                return shift_horizontal(maze, move[1], robot, empty)
            else:
                debug_print("    Can't move")
                return robot
        else:
            debug_print("    Vertical move")
            r = Range(robot[1], robot[1], robot[0])
            boxes = find_boxes_to_move(maze, [r], move[0])
            if boxes is not None:
                debug_print("      Moving boxes")
                move_boxes_vertically(maze, boxes, move[0])
                return move_robot(maze, robot, next_pos)
            else:
                debug_print("    Can't move")
                return robot
    else:
        raise Exception("This should not happen")


def is_horizontal(move):
    return move[0] == 0


def shift_horizontal(maze, step, robot, empty):
    pos = empty
    reverse = step * -1
    next_pos = get_next_pos(pos, (0, reverse))
    while pos != robot:
        maze[pos[0]][pos[1]] = maze[next_pos[0]][next_pos[1]]
        pos = next_pos
        next_pos = get_next_pos(next_pos, (0, reverse))
    maze[robot[0]][robot[1]] = EMPTY

    return robot[0], robot[1] + step


def get_next_pos(robot, move):
    return robot[0] + move[0], robot[1] + move[1]


def find_boxes_to_move(maze, ranges: list[Range], vertical_direction):
    visited_ranges = []
    while ranges:
        r = ranges.pop()
        visited_ranges.append(r)
        new_ranges = find_ranges_with_boxes(maze, r.in_direction(vertical_direction))
        if new_ranges is None:
            return None
        ranges.extend(new_ranges)

    boxes = []
    for r in visited_ranges:
        boxes.extend(get_boxes_in_range(maze, r))

    return boxes


def find_ranges_with_boxes(maze: list[list[str]], r: Range):
    ranges = []
    current_range: Range | None = None
    for x in range(r.start_x, r.end_x + 1):
        if maze[r.y][x] == WALL:
            return None
        elif maze[r.y][x] == EMPTY:
            if current_range is not None:
                ranges.append(current_range)
                current_range = None
        else:
            box_range = get_box_range(maze, (r.y, x))
            if box_range is not None:
                if current_range is None:
                    current_range = box_range
                else:
                    current_range.extend(box_range)
    if current_range is not None:
        ranges.append(current_range)
    return ranges


def get_box_range(maze: list[list[str]], pos: tuple[int, int]):
    if maze[pos[0]][pos[1]] == BOX:
        return Range(pos[1], pos[1], pos[0])
    elif maze[pos[0]][pos[1]] == BOX_LEFT:
        return Range(pos[1], pos[1] + 1, pos[0])
    elif maze[pos[0]][pos[1]] == BOX_RIGHT:
        return Range(pos[1] - 1, pos[1], pos[0])
    else:
        return None


def get_boxes_in_range(maze: list[list[str]], r: Range):
    boxes = []
    x = r.start_x
    while x <= r.end_x:
        if maze[r.y][x] == BOX:
            boxes.append(Range(x, x, r.y))
        elif maze[r.y][x] == BOX_LEFT:
            boxes.append(Range(x, x + 1, r.y))
            x += 1
        x += 1
    return boxes


def move_boxes_vertically(maze, boxes, dy):
    clear_old_box_positions(maze, boxes)
    for box in boxes:
        maze[box.y + dy][box.start_x] = BOX_LEFT
        maze[box.y + dy][box.end_x] = BOX_RIGHT


def clear_old_box_positions(maze, boxes):
    for box in boxes:
        maze[box.y][box.start_x] = EMPTY
        maze[box.y][box.end_x] = EMPTY


def move_robot(maze, robot, next_pos):
    maze[robot[0]][robot[1]] = EMPTY
    maze[next_pos[0]][next_pos[1]] = ROBOT
    return next_pos


def find_first_empty(maze, pos, move):
    while maze[pos[0]][pos[1]] != EMPTY and maze[pos[0]][pos[1]] != WALL:
        pos = get_next_pos(pos, move)
    return pos if maze[pos[0]][pos[1]] != WALL else None


def is_box(maze, pos):
    c = maze[pos[0]][pos[1]]
    return c == BOX_LEFT or c == BOX_RIGHT or c == BOX


EMPTY = "."
WALL = "#"
ROBOT = "@"
BOX = "O"
BOX_LEFT = "["
BOX_RIGHT = "]"
DIR = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1)
}


def read_input(input_file_name):
    maze = []
    commands = ""
    with open(input_file_name, "r") as f:
        lines = read_until_empty_line(f)
        for line in lines:
            maze.append(list(line.strip("\n")))
        lines = read_until_empty_line(f)
        for line in lines:
            commands += line.replace("\n", "")
    return maze, commands


def read_until_empty_line(f):
    lines = []
    while True:
        line = f.readline().strip("\n")
        if line == "":
            break
        lines.append(line)
    return lines


def print_maze(maze):
    for line in maze:
        debug_print("".join(line))


def get_gps_positions(maze):
    position_sum = 0
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == BOX or maze[i][j] == BOX_LEFT:
                position_sum += 100 * i + j
    return position_sum


DEBUG = False


def debug_print(*args):
    if DEBUG:
        print(*args)


if __name__ == "__main__":
    main()