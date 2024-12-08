use_example_input = False

EMPTY = "."

def main():
    maze = read_input()
    antennas = find_antennas(maze)
    count_antinodes(maze, antennas, 1, 1)
    count_antinodes(maze, antennas, 0, 999)

def read_input():
    file_name = "example08.txt" if use_example_input else "input08.txt"
    with open(file_name, "r") as f:
        return f.read().splitlines()

def find_antennas(maze):
    antennas = {}
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            char = maze[row][col]
            if char != EMPTY:
                if not char in antennas:
                    antennas[char] = []
                antennas[char].append((row, col))
    return antennas

def count_antinodes(maze, antennas, min_harmonics, max_harmonics):
    antinodes = get_antinode_locations(maze, antennas, min_harmonics, max_harmonics)
    print_maze(maze)
    print(len(antinodes))

def get_antinode_locations(maze, antennas, min_harmonics, max_harmonics):
    rows = len(maze)
    cols = len(maze[0])
    antinode_locations = set()
    for a in antennas:
        locations = antennas[a]
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                antinodes = get_antinodes(locations[i], locations[j], min_harmonics, max_harmonics, rows, cols)
                for antinode in antinodes:
                    debug_add_antinode(maze, antinode)
                    antinode_locations.add(antinode)
    return antinode_locations

def get_antinodes(p1, p2, min_harmonics, max_harmonics, rows, cols):
    dr = p1[0] - p2[0]
    dc = p1[1] - p2[1]
    antinodes = []
    for i in range(min_harmonics, max_harmonics + 1):
        p = (p1[0] + i * dr, p1[1] + i * dc)
        if not is_within_bounds(p, rows, cols):
            break
        antinodes.append(p)
    for i in range(min_harmonics, max_harmonics + 1):
        p = (p2[0] - i * dr, p2[1] - i * dc)
        if not is_within_bounds(p, rows, cols):
            break
        antinodes.append(p)
    return antinodes

def is_within_bounds(pos, rows, cols):
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols

def debug_add_antinode(maze, antinode):
    maze[antinode[0]] = maze[antinode[0]][:antinode[1]] + "#" + maze[antinode[0]][antinode[1]+1:]

def print_maze(maze):
    for line in maze:
        print(line)

if __name__ == "__main__":
    main()
