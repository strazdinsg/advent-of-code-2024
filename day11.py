use_example_input = False

EMPTY = -1

class TreeNode:
    def __init__(self, value: int):
        self.value = value
        self.cached_counts = dict()
        self.children = []
    
    def add_child(self, child_node):
        self.children.append(child_node)
    
    def __str__(self):
        return f"{self.value}: {' '.join([str(child.value) for child in self.children])}"
    
    def count_visited(self, steps: int):
        if steps == 0:
            return 1
        if steps in self.cached_counts:
            return self.cached_counts[steps]
        count = 0
        for child in self.children:
            count += child.count_visited(steps - 1)        
        self.cached_counts[steps] = count
        return count
    
def main():
    stones = read_input()
    graph = build_graph(stones)
    part1 = graph.count_visited(25 + 1)
    print(part1)
    part2 = graph.count_visited(75 + 1)
    print(part2)

def build_graph(stones: list[int]):
    to_visit: list[TreeNode] = []
    nodes: dict[int:TreeNode] = dict()
    graph = TreeNode(EMPTY)
    for stone in stones:
        v = TreeNode(stone)
        graph.add_child(v)
        to_visit.append(v)
    while to_visit:
        v = to_visit.pop()
        next_values = blink(v.value)
        for n in next_values:
            if not n in nodes:
                nodes[n] = TreeNode(n)
                to_visit.append(nodes[n])
            child = nodes[n]
            v.add_child(child)
        nodes[v.value] = v
    return graph

def blink(stone: int):
    if stone == 0:
        return [1]
    elif even_digits(stone):
        return get_parts(stone)
    else:
        return [stone * 2024]

def read_input():
    file_name = "example11.txt" if use_example_input else "input11.txt"
    with open(file_name, "r") as f:
        return list(map(int, f.readline().split()))


def even_digits(stone):
    return len(str(stone)) % 2 == 0

def get_parts(value):
    s = str(value)
    half = len(s) // 2
    return [int(s[:half]), int(s[half:])]

if __name__ == "__main__":
    main()
