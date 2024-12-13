use_example_input = False

empty_garden = []

def main():
    garden = read_input()
    create_empty_garden_copy(garden)
    print_garden(garden)
    regions = find_regions(garden)
    simple_price = 0
    print(f"{len(regions)} regions in total")
    for region in regions:
        simple_price += region.get_price()
    print("Part 1:", simple_price)
    discounted_price = 0
    for i in range(len(regions)):
        region = regions[i]
        print(f"Processing region {i}")
        discounted_price += region.get_discounted_price()
    print("Part 2:", discounted_price)

def read_input():
    file_name = "example12.txt" if use_example_input else "input12.txt"
    with open(file_name, "r") as f:
        garden = []
        line = f.readline().strip()
        while line != "":
            garden.append(list(line))
            line = f.readline().strip()
        return garden

VISITED = "+"
EXTERNAL = "@"
EMPTY="."

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
OUTSIDE = {
    UP: DLEFT, 
    RIGHT: DUP,
    DOWN: DRIGHT,
    LEFT: DDOWN
}


class Region:
    def __init__(self, char, garden_rows, garden_cols):
        self.char = char
        self.top_left = None
        self.plots = {}
        self.garden_rows = garden_rows
        self.garden_cols = garden_cols

    def add_plot(self, pos, fences) -> None:
        if self.top_left is None:
            self.top_left = pos
        self.plots[pos] = fences

    def get_price(self):
        return self.get_area() * self.get_perimeter()

    def get_area(self):
        return len(self.plots)

    def get_perimeter(self):
        perimeter = 0
        for pos in self.plots:
            perimeter += len(self.plots[pos])
        return perimeter

    def get_discounted_price(self):
        return self.get_area() * self.get_side_count()
    
    def get_side_count(self):
        return self.get_external_side_count() + self.get_internal_side_count()

    def get_external_side_count(self):
        pos = self.top_left
        d = RIGHT
        sides = 0
        while True:
            pos = self.find_last_pos_on_contour(pos, d)
            sides += 1
            if self.has_outside_plot(pos, d):
                d = turn_counter_clockwise(d)
                pos = get_next_pos(pos, d)
            else:
                d = turn_clockwise(d)
            if pos == self.top_left and d == RIGHT:
                break
        return sides

    def find_last_pos_on_contour(self, pos, d):
        next_pos = get_next_pos(pos, d)
        while next_pos in self.plots and not self.has_outside_plot(pos, d):
            pos = next_pos
            next_pos = get_next_pos(pos, d)
        return pos
    
    def has_outside_plot(self, pos, d):
        outside = get_outside_pos(pos, d)
        return outside in self.plots

    def get_internal_side_count(self):
        garden = self.prepare_garden_copy()
        mark_outside_cells(garden)
        sides = 0
        for row in range(len(garden)):
            for col in range(len(garden[0])):
                cell = garden[row][col]
                if cell == EMPTY:
                    sides += measure_internal_hole(garden, (row, col))
        return sides

    def prepare_garden_copy(self):
        global empty_garden
        garden = []
        for line in empty_garden:
            garden.append(line.copy())
        for plot in self.plots:
            garden[plot[0]][plot[1]] = self.char
        return garden

def find_regions(garden):
    regions = []
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if garden[i][j] != VISITED:
                regions.append(find_region(garden, i, j))
    return regions

def find_region(garden, i, j):
    c = garden[i][j]
    region = Region(c, len(garden), len(garden[0]))
    to_visit = [(i, j)]
    visited = set()
    while to_visit:
        pos = to_visit.pop()
        visited.add(pos)
        fences = set()
        for direction in DIRECTIONS:
            d = DIRECTIONS[direction]
            next_pos = (pos[0] + d[0], pos[1] + d[1])
            if is_same_region(garden, next_pos, c):
                if next_pos not in visited and next_pos not in to_visit:
                    to_visit.append(next_pos)
            else:
                fences.add(direction)
        region.add_plot(pos, fences)
    for v in visited:
        garden[v[0]][v[1]] = VISITED
    return region

def is_within_bounds(garden, pos):
    return 0 <= pos[0] < len(garden) \
        and 0 <= pos[1] < len(garden[0])

def is_same_region(garden, pos, plot_char):
    return is_within_bounds(garden, pos) and garden[pos[0]][pos[1]] == plot_char

def print_garden(garden):
    for line in garden:
        print("".join(line))

def turn_counter_clockwise(d):
    return (d - 1) % 4

def turn_clockwise(d):
    return (d + 1) % 4

def get_next_pos(pos, d):
    next_dir = DIRECTIONS[d]
    return pos[0] + next_dir[0], pos[1] + next_dir[1]


def get_outside_pos(pos: tuple[int, int], d: int):
    outside_dir = OUTSIDE[d]
    return pos[0] + outside_dir[0], pos[1] + outside_dir[1]

def create_empty_garden_copy(garden):
    global empty_garden
    empty_line = []
    for col in range(len(garden[0])):
        empty_line.append(EMPTY)
    for row in range(len(garden)):
        empty_garden.append(empty_line.copy())

def mark_outside_cells(garden):
    rows = len(garden)
    cols = len(garden[0])
    for row in range(rows):
        if garden[row][0] == EMPTY:
            mark_as_outside(garden, row, 0)
        if garden[row][cols - 1] == EMPTY:
            mark_as_outside(garden, row, cols - 1)
    for col in range(cols):
        if garden[0][col] == EMPTY:
            mark_as_outside(garden, 0, col)
        if garden[rows - 1][col] == EMPTY:
            mark_as_outside(garden, rows - 1, col)

def mark_as_outside(garden, row, col):
    mark_as(garden, (row, col), EXTERNAL)

def mark_as_visited(garden, pos):
    mark_as(garden, pos, VISITED)

def mark_as(garden, pos, marker):
    to_visit = [pos]
    while to_visit:
        pos = to_visit.pop()
        garden[pos[0]][pos[1]] = marker
        for d in DIRECTIONS:
            next_pos = get_next_pos(pos, d)
            if is_empty(garden, next_pos):
                to_visit.append(next_pos)

def is_empty(garden, pos):
    return is_within_bounds(garden, pos) and garden[pos[0]][pos[1]] == EMPTY

def measure_internal_hole(garden, top_left_pos):
    pos = top_left_pos
    d = RIGHT
    sides = 0
    while True:
        pos = find_last_pos_on_empty_contour(garden, pos, d)
        sides += 1
        if has_outside_empty_plot(garden, pos, d):
            d = turn_counter_clockwise(d)
            pos = get_next_pos(pos, d)
        else:
            d = turn_clockwise(d)
        if pos == top_left_pos and d == RIGHT:
            break
    mark_as_visited(garden, top_left_pos)
    return sides

def find_last_pos_on_empty_contour(garden, pos, d):
    next_pos = get_next_pos(pos, d)
    while is_empty(garden, next_pos) and not has_outside_empty_plot(garden, pos, d):
        pos = next_pos
        next_pos = get_next_pos(pos, d)
    return pos

def has_outside_empty_plot(garden, pos, d):
    return is_empty(garden, get_outside_pos(pos, d))


if __name__ == "__main__":
    main()
