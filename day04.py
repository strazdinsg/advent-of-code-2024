use_example_input = False

def main():
    read_input()
    print(count_xmas())
    print(count_xmas_2())

puzzle = []

def read_input():
    file_name = "example04.txt" if use_example_input else "input04.txt"
    with open(file_name, "r") as f:
        global puzzle
        puzzle = f.read().splitlines()

def count_xmas():
    count = 0
    col_count = len(puzzle[0])
    for row in range(len(puzzle)):
        for col in range(col_count):
            if puzzle[row][col] == "X":
                count += is_xmas(row, col)
    return count

def is_xmas(r, c):
    count = 0
    if is_letter("M", r, c + 1) and is_letter("A", r, c + 2) and is_letter("S", r, c + 3):
        count += 1 # RIGHT
    if is_letter("M", r + 1, c) and is_letter("A", r + 2, c) and is_letter("S", r + 3, c):
        count += 1 # DOWN
    if is_letter("M", r, c - 1) and is_letter("A", r, c - 2) and is_letter("S", r, c - 3):
        count += 1 # LEFT
    if is_letter("M", r - 1, c) and is_letter("A", r - 2, c) and is_letter("S", r - 3, c):
        count += 1 # UP
    if is_letter("M", r - 1, c + 1) and is_letter("A", r - 2, c + 2) and is_letter("S", r - 3, c + 3):
        count += 1 # UPRIGHT
    if is_letter("M", r - 1, c - 1) and is_letter("A", r - 2, c - 2) and is_letter("S", r - 3, c - 3):
        count += 1 # UPLEFT
    if is_letter("M", r + 1, c + 1) and is_letter("A", r + 2, c + 2) and is_letter("S", r + 3, c + 3):
        count += 1 # DOWNRIGHT
    if is_letter("M", r + 1, c - 1) and is_letter("A", r + 2, c - 2) and is_letter("S", r + 3, c - 3):
        count += 1 # DOWNLEFT
    return count

def is_letter(letter, row, col):
    return row >= 0 and row < len(puzzle) and col >= 0 and col < len(puzzle[0]) and puzzle[row][col] == letter

def count_xmas_2():
    count = 0
    for row in range(1, len(puzzle) - 1):
        for col in range(1, len(puzzle[0]) - 1):
            if puzzle[row][col] == "A" and is_xmas_cross(row, col):
                count += 1
    return count

def is_xmas_cross(row, col):
    return is_mas_right_down(row, col) and is_mas_right_up(row, col)

def is_mas_right_down(r, c):
    return (is_letter("M", r - 1, c - 1) and is_letter("S", r + 1, c + 1)) or \
           (is_letter("M", r + 1, c + 1) and is_letter("S", r - 1, c - 1))

def is_mas_right_up(r, c):
    return (is_letter("M", r - 1, c + 1) and is_letter("S", r + 1, c - 1)) or \
           (is_letter("M", r + 1, c - 1) and is_letter("S", r - 1, c + 1))

if __name__ == "__main__":
    main()
