use_example_input = False


def main():
    garden = read_input()
    rows = len(garden)
    cols = len(garden[0])
    simple_price = 0
    discounted_price = 0
    for row in range(rows):
        for col in range(cols):
            if garden[row][col] != VISITED:
                perimeter, sides, area = visit_region(garden, row, col)
                simple_price += perimeter * area
                discounted_price += sides * area
    print(f"Part 1: {simple_price}")
    print(f"Part 2: {discounted_price}")


def visit_region(garden, row, col):
    plant_type = garden[row][col]
    visited = set()
    to_visit = [(row, col)]
    perimeter = 0
    contour = {UP: set(), RIGHT: set(), DOWN: set(), LEFT: set()}
    while to_visit:
        pos = to_visit.pop()
        visited.add(pos)
        for direction in DIRECTIONS:
            d = DIRECTIONS[direction]
            next_pos = (pos[0] + d[0], pos[1] + d[1])
            if is_plant(garden, next_pos, plant_type):
                if next_pos not in visited and next_pos not in to_visit:
                    to_visit.append(next_pos)
            else:
                contour[direction].add(pos)
                perimeter += 1
    for v in visited:
        garden[v[0]][v[1]] = VISITED
    area = len(visited)
    sides = 0
    for direction in DIRECTIONS:
        while contour[direction]:
            c = contour[direction]
            sides += 1
            to_visit = [c.pop()]
            while to_visit:
                pos = to_visit.pop()
                for d in DIRECTIONS.values():
                    next_pos = (pos[0] + d[0], pos[1] + d[1])
                    if next_pos in c and next_pos not in to_visit:
                        to_visit.append(next_pos)
                        c.remove(next_pos)
    return perimeter, sides, area


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

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

DUP = (-1, 0)
DRIGHT = (0, 1)
DDOWN = (1, 0)
DLEFT = (0, -1)
DIRECTIONS = {
    UP: DUP, 
    RIGHT: DRIGHT,
    DOWN: DDOWN,
    LEFT: DLEFT
}


def is_plant(garden, pos, plant_type):
    return 0 <= pos[0] < len(garden) and 0 <= pos[1] < len(garden[0]) and garden[pos[0]][pos[1]] == plant_type


if __name__ == "__main__":
    main()
