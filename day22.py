from collections import deque

use_example_input = False

STEPS = 2000
DIFF_SIZE = 4

all_combos = set()


class Secret:
    def __init__(self, n):
        self.n = n
        self.combos = {}
        self.diffs = deque(maxlen=DIFF_SIZE)
        self.price = self.n % 10

    def next(self):
        prev_price = self.price
        self.mix(self.n * 64)
        self.prune()
        self.mix(self.n // 32)
        self.prune()
        self.mix(self.n * 2048)
        self.prune()
        self.price = self.n % 10
        self.save_combo(prev_price)

    def get_value(self):
        return self.n

    def mix(self, value):
        self.n = self.n ^ value

    def prune(self):
        self.n = self.n % 16777216

    def save_combo(self, prev_price):
        global all_combos
        diff = self.price - prev_price
        self.diffs.append(diff)
        if len(self.diffs) == DIFF_SIZE:
            d = tuple(self.diffs)
            if d not in self.combos:
                self.combos[d] = self.price
                all_combos.add(d)

    def get_price_for_combo(self, combo):
        return self.combos[combo] if combo in self.combos else 0


def main():
    input_file_name = "example22.txt" if use_example_input else "input22.txt"
    secrets = read_input(input_file_name)
    price_sum = 0
    for secret in secrets:
        for i in range(STEPS):
            secret.next()
        price_sum += secret.get_value()
    print(f"Part1: {price_sum}")
    best_combo_price = get_best_combo(secrets)
    print(f"Part2: {best_combo_price}")


def read_input(input_file_name):
    with open(input_file_name, "r") as f:
        return [Secret(int(line)) for line in f.readlines()]


def get_best_combo(secrets):
    best_price = 0
    for combo in all_combos:
        price = 0
        relevant_secrets = []
        for secret in secrets:
            p = secret.get_price_for_combo(combo)
            if p > 0:
                price += p
                relevant_secrets.append(secret)
        if price > best_price:
            best_price = price
    return best_price


if __name__ == "__main__":
    main()
