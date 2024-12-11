use_example_input = False

EMPTY = -1

class TreeNode:
    def __init__(self, data, child_values):
        self.data = data
        self.children = [TreeNode(v, []) for v in child_values]
    def split_into_two(self, value1, value2):
        self.data = EMPTY
        self.children = [TreeNode(value1, []), TreeNode(value2, [])]
    def count(self):
        count = 1 if self.data != EMPTY else 0
        for c in self.children:
            count += c.count()
        return count
    def debug_print(self):    
        print(self.get_debug_string())    
    def get_debug_string(self):
        if self.data != EMPTY:
            return str(self.data)
        else:
            return ' '.join([c.get_debug_string() for c in self.children])
    def blink(self):
        if self.data != EMPTY:
            if self.data == 0:
                self.data = 1
            elif even_digits(self.data):
                p1, p2 = get_parts(self.data)
                self.split_into_two(p1, p2)
            else:
                self.data *= 2024
        else:
            for c in self.children:
                c.blink()

def even_digits(stone):
    return len(str(stone)) % 2 == 0

def get_parts(value):
    s = str(value)
    half = len(s) // 2
    return int(s[:half]), int(s[half:])


def main():
    stones = read_input()
    stones.debug_print()
    keep_blinking(stones, 25)
    print("Part 1:", stones.count())
    print("Part 2 is too slow, need a different approach :(")


def keep_blinking(stones, count):
    i = 0
    while i < count:
        stones.blink()
        i += 1
        # stones.debug_print()
        # print(stones.count())
        # print(i, "steps done")


def read_input():
    file_name = "example11.txt" if use_example_input else "input11.txt"
    with open(file_name, "r") as f:
        return TreeNode(EMPTY, list(map(int, f.readline().split())))




if __name__ == "__main__":
    main()
