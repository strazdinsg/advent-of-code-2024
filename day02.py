use_example_input = False


def main():
    reports = read_reports()
    print_safe_count(reports, False)
    print_safe_count(reports, True)


def print_safe_count(reports, try_remove_one):
    safe_count = sum(1 for report in reports if is_safe(report, try_remove_one))
    print("Answer with %s: %d" % ("removing one level" if try_remove_one else "no removing", safe_count))


def is_safe(report, try_remove_one):
    l = [report]
    if try_remove_one:
        for i in range(len(report)):
            l.append(report[:i] + report[i+1:])
    return any(is_increasing(list_to_check) or is_decreasing(list_to_check) for list_to_check in l)


def is_increasing(report):
    return is_safe_internal(report, 1, 3)


def is_decreasing(report):
    return is_safe_internal(report, -3, -1)


def is_safe_internal(report, min_diff, max_diff):
    return all(min_diff <= report[i] - report[i-1] <= max_diff for i in range(1, len(report)))


def read_reports():
    file_name = "example02.txt" if use_example_input else "input02.txt"
    reports = []
    with open(file_name, "r") as f:
        for line in f:
            reports.append(list(map(int, line.split())))
    return reports


if __name__ == "__main__":
    main()
