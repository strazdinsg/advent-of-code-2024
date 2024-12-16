from collections import Counter

example = False

file_name = "example01.txt" if example else "input01.txt"
a = []
b = []
with open(file_name, "r") as f:
    for line in f:
        num1, num2 = map(int, line.split())
        a.append(num1)
        b.append(num2)

sorted_a = sorted(a)
sorted_b = sorted(b)

s = 0
for i in range(len(sorted_a)):
    s += abs(sorted_a[i] - sorted_b[i])

print("Answer for part 1: %d" % s)

bag_b = Counter(b)

bag_sum = 0
for i in a:
    bag_sum += i * bag_b[i]

print("Answer for part 2: %d" % bag_sum)
