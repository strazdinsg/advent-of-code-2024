use_example_input = True

def main():
    garden = read_input()
    print_garden(garden)
    regions = find_regions(garden)
    simple_price = 0
    for region in regions:
        simple_price += region.get_price()
    print("Part 1:", simple_price)
    discounted_price = 0
    for region in regions:
        dp = region.get_discounted_price()
        print(dp)
        discounted_price += dp
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
OUTSIDE = {
    UP: DLEFT, 
    RIGHT: DUP,
    DOWN: DRIGHT,
    LEFT: DDOWN
}


class Region:
    def __init__(self) -> None:
        self.top_left = None
        self.plots = {}

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
        sides = 0
        pos = self.top_left
        d = RIGHT
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
        next = get_next_pos(pos, d)
        while next in self.plots and not self.has_outside_plot(pos, d):
            pos = next
            next = get_next_pos(pos, d)
        return pos
    
    def has_outside_plot(self, pos, d):
        outside = get_outside_pos(pos, d)
        return outside in self.plots



def find_regions(garden):
    regions = []
    for i in range(len(garden)):
        for j in range(len(garden[0])):
            if garden[i][j] != VISITED:
                regions.append(find_region(garden, i, j))
    return regions


def find_region(garden, i, j):
    c = garden[i][j]
    region = Region()
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

def is_same_region(garden, pos, plot_char):
    return 0 <= pos[0] < len(garden) \
        and 0 <= pos[1] < len(garden[0]) \
        and garden[pos[0]][pos[1]] == plot_char

def print_garden(garden):
    for line in garden:
        print("".join(line))

def turn_counter_clockwise(dir):
    return (dir - 1) % 4

def turn_clockwise(dir):
    return (dir + 1) % 4

def get_next_pos(pos, dir):
    next_dir = DIRECTIONS[dir]
    return pos[0] + next_dir[0], pos[1] + next_dir[1]


def get_outside_pos(pos: tuple[int, int], d: int):
    outside_dir = OUTSIDE[d]
    return pos[0] + outside_dir[0], pos[1] + outside_dir[1]


if __name__ == "__main__":
    main()
