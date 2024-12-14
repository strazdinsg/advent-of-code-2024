import re


use_example_input = False

HEIGHT = 7 if use_example_input else 103
WIDTH = 11 if use_example_input else 101
SIMULATION_LENGTH = 10000
SHORT_SIMULATION_LENGTH = 100


def main():
    robots = read_input()
    for i in range(SIMULATION_LENGTH):
        simulate_move(robots)
        # I noticed there is a bit different pattern after 99 moves, then 200 moves, 301 moves, etc.
        # So I printed each 101st frame with offset 98
        # This is how I found out that the Christmas tree is in frame number 7371
        # if (i - 98) % 101 == 0:
        #     print_robots_to_file(i + 1, robots)
        if i == 7370:
            print_robots_to_file(i + 1, robots)
            break
        elif i == SHORT_SIMULATION_LENGTH - 1:
            print(count_in_quadrants(robots))
    print_robots(robots)


def simulate_move(robots):
    for i in range(len(robots)):
        x, y, mx, my = robots[i]
        x = (x + mx) % WIDTH
        y = (y + my) % HEIGHT
        robots[i] = (x, y, mx, my)


def count_in_quadrants(robots):
    counts = {(False, False): 0, (False, True): 0, (True, False): 0, (True, True): 0}
    middle_x = WIDTH // 2
    middle_y = HEIGHT // 2
    for x, y, mx, my in robots:
        if x == middle_x or y == middle_y:
            continue
        quadrant = (x > middle_x, y > middle_y)
        counts[quadrant] += 1
    multiplication = 1
    for count in counts.values():
        multiplication *= count
    return multiplication


def read_input():
    file_name = "example14.txt" if use_example_input else "input14.txt"
    with open(file_name, "r") as f:
        robots = []
        lines = f.readlines()
        for line in lines:
            matches = re.findall(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
            robots.append([int(s) for s in matches[0]])
        return robots


def print_robots(robots):
    robot_map = get_robot_map_debug(robots)
    for line in robot_map:
        print(line)


def get_robot_map_debug(robots):
    counts = []
    for i in range(HEIGHT):
        counts.append([0 for _ in range(WIDTH)])
    for x, y, mx, my in robots:
        counts[y][x] = counts[y][x] + 1
    lines = []
    for i in range(HEIGHT):
        line = ""
        for j in range(WIDTH):
            if counts[i][j] > 0:
                line += str(counts[i][j])
            else:
                line += "."
        lines.append(line)
    return lines


def print_robots_to_file(move_count, robots):
    with open("debug14.txt", "w") as f:
        f.write(f"{move_count}:\n")
        robot_map = get_robot_map_debug(robots)
        for line in robot_map:
            f.write(line)
            f.write("\n")


if __name__ == "__main__":
    main()
