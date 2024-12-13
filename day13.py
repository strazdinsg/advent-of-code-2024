use_example_input = False

def main():
    machines = read_input()
    get_cheapest_sum(machines, 0)
    get_cheapest_sum(machines, 10000000000000)

A_COST = 3
B_COST = 1

class Machine:
    def __init__(self, a, b, prize):
        self.a1 = a[0]
        self.a2 = a[1]
        self.b1 = b[0]
        self.b2 = b[1]
        self.c1 = prize[0]
        self.c2 = prize[1]

    def get_cheapest_prize(self, prize_offset):
        c1 = self.c1 + prize_offset
        c2 = self.c2 + prize_offset
        # Solve this equation:
        # |a1 b1| * |a| = |c1|
        # |a2 b2|   |b|   |c2|

        determinant = self.a1 * self.b2 - self.a2 * self.b1
        if determinant == 0:
            return 0

        # Use Cramer's rule
        a = (c1 * self.b2 - c2 * self.b1) // determinant
        b = (self.a1 * c2 - self.a2 * c1) // determinant

        # Check whether the solution is in integers
        if a * self.a1 + b * self.b1 != c1 or \
            a * self.a2 + b * self.b2 != c2:
            return 0

        return int(a * A_COST + b * B_COST)

def get_cheapest_sum(machines, prize_offset):
    cheapest_sum = 0
    for machine in machines:
        cheapest = machine.get_cheapest_prize(prize_offset)
        cheapest_sum += cheapest
    print(cheapest_sum)


def read_input():
    file_name = "example13.txt" if use_example_input else "input13.txt"
    with open(file_name, "r") as f:
        machines = []
        machine = read_machine_input(f)
        while machine is not None:
            machines.append(machine)
            machine = read_machine_input(f)
        return machines

def read_machine_input(f):
    a = read_button_line(f)
    b = read_button_line(f)
    prize = read_prize_line(f)
    if a is None or b is None or prize is None:
        return None
    f.readline()
    return Machine(a, b, prize)

def read_button_line(f):
    return read_two_number_line(f, 12, ", Y+")

def read_prize_line(f):
    return read_two_number_line(f, 9, ", Y=")

def read_two_number_line(f, offset, separator):
    line = f.readline().strip()
    if line == "":
        return None
    parts = list(map(int, line[offset:].split(separator)))
    return parts

if __name__ == "__main__":
    main()
