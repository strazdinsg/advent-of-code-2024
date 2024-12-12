use_example_input = False

def main():
    garden = read_input()
    # print_garden(garden)
    regions = find_regions(garden)
    total_price = 0
    for region in regions:
        total_price += get_price(region)
    print("Part 1:", total_price)

def read_input():
    file_name = "example12.txt" if use_example_input else "input12.txt"
    with open(file_name, "r") as f:
        garden = []
        line = f.readline().strip()
        while line != "":
            garden.append(list(line))
            line = f.readline().strip()
        return garden

VISITED = "."

def find_regions(garden):
    regions = []
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if (garden[i][j] != VISITED):
                regions.append(find_region(garden, i, j))
    return regions

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

def find_region(garden, i, j):
    c = garden[i][j]
    region = []
    to_visit = [(i, j)]
    visited = set()
    while to_visit:
        (i, j) = to_visit.pop()
        visited.add((i, j))
        fence_count = 0
        for dir in DIRECTIONS:
            next = (i + dir[0], j + dir[1])
            if is_same_region(garden, next, c):
                if next not in visited and next not in to_visit:
                    to_visit.append(next)
            else:
                fence_count += 1
        region.append((i, j, fence_count))
    for v in visited:
        garden[v[0]][v[1]] = VISITED
    return region

def is_same_region(garden, pos, plot_char):
    return 0 <= pos[0] < len(garden) \
        and 0 <= pos[1] < len(garden[0]) \
        and garden[pos[0]][pos[1]] == plot_char

def print_garden(garden):
    for line in garden:
        print("".join(line))

def get_price(region):
    perimeter = 0
    for plot in region:
        perimeter += plot[2]
    area = len(region)
    return area * perimeter

if __name__ == "__main__":
    main()
