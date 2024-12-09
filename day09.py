use_example_input = False

EMPTY = -1

def main():
    compressed_disk_map = read_input()
    disk_map = decompress_disk(compressed_disk_map)
    # Part 1
    fragmented_disk = fragment_disk(disk_map)
    fragmented_hash = calculate_hash(fragmented_disk)
    print(fragmented_hash)
    # Part 2
    compacted_disk = compact_disk(disk_map)
    compact_hash = calculate_hash(compacted_disk)
    print(compact_hash)

def read_input():
    file_name = "example09.txt" if use_example_input else "input09.txt"
    with open(file_name, "r") as f:
        return f.read(20000)

def decompress_disk(compressed_disk_map):
    disk_map = []
    is_empty = False
    block_id = 0
    for block_len in compressed_disk_map:
        for _ in range(int(block_len)):
            if is_empty:
                disk_map.append(EMPTY)
            else:
                disk_map.append(block_id)
        if is_empty:
            is_empty = False
            block_id += 1
        else:
            is_empty = True
    return disk_map
        
def fragment_disk(disk_map):
    d = disk_map.copy()
    head_pos = 0
    while head_pos < len(d):
        if d[head_pos] == EMPTY:
            move_last_block(d, head_pos)
        head_pos += 1
    return d

def move_last_block(disk_map, head_pos):
    disk_map[head_pos] = disk_map.pop()
    strip_empty_blocks(disk_map)

def strip_empty_blocks(disk_map):
    while disk_map[-1] == EMPTY:
        disk_map.pop()

def calculate_hash(disk_map):
    hash = 0
    for i in range(len(disk_map)):
        if disk_map[i] != EMPTY:
            hash += i * disk_map[i]
    return hash

def compact_disk(disk_map):
    d = disk_map.copy()
    range_start, range_len = get_movable_range(d, len(d) - 1)
    while range_len > 0:
        empty_start = find_first_empty_range(d, range_len)
        if empty_start < range_start:
            move_last_block_range(d, range_start, range_len, empty_start)
        range_start, range_len = get_movable_range(d, range_start - 1)
    return d

def find_first_empty_range(disk_map, min_length):
    head = 0
    found_len = 0
    while head < len(disk_map):
        found_len = found_len + 1 if disk_map[head] == EMPTY else 0
        if found_len == min_length:
            return head - found_len + 1
        head += 1

    return head

def get_movable_range(disk_map, start_index):
    head = start_index
    while head >= 0 and disk_map[head] == EMPTY:
        head -= 1
    block_id = disk_map[head]
    range_end = head
    while head >= 0 and disk_map[head] == block_id:
        head -= 1
    range_len = range_end - head if head >= 0 else -1        
    return head + 1, range_len

def move_last_block_range(disk_map, range_start, range_len, empty_range_start):
    head_empty = empty_range_start
    head_range = range_start
    while range_len > 0:
        disk_map[head_empty] = disk_map[head_range]
        disk_map[head_range] = EMPTY
        head_empty += 1
        head_range += 1
        range_len -= 1

if __name__ == "__main__":
    main()
