use_example_input = False

def main():
    rules, updates = read_input()
    mid_sum, mid_sum_broken = count_mid_sum(rules, updates)
    print(mid_sum)
    print(mid_sum_broken)

def count_mid_sum(rules, updates):
    mid_sum = 0
    mid_sum_broken = 0
    for update in updates:
        broken = False
        for i in range(1, len(update)):
            for j in range(i):
                first = update[j]
                second = update[i]
                if second in rules and first in rules[second]:
                    broken = True
                    temp = update[i]
                    update[i] = update[j]
                    update[j] = temp
        mid_value = update[len(update) // 2]
        if broken:
            mid_sum_broken += mid_value
        else:
            mid_sum += mid_value
    return mid_sum, mid_sum_broken

def read_input():
    file_name = "example05.txt" if use_example_input else "input05.txt"
    with open(file_name, "r") as f:
        lines = f.read().splitlines()
        rules = {}
        updates = []
        reading_rules = True
        for line in lines:
            if line == "":
                reading_rules = False
                continue
            if reading_rules:
                parts = line.split("|")
                key = int(parts[0])
                if key not in rules:
                    rules[key] = set()
                rules[key].add(int(parts[1]))
            else:
                updates.append(list(map(int, line.split(","))))
        return rules, updates

if __name__ == "__main__":
    main()
