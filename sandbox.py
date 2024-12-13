import heapq

# Initialize an empty heap
heap = []

# Adding elements to the heap
heapq.heappush(heap, 5)
heapq.heappush(heap, 3)
heapq.heappush(heap, 8)
heapq.heappush(heap, 1)
heapq.heappush(heap, 6)

# Print the heap (heapq doesn't guarantee full sorting, just heap structure)
print("Heap after adding elements:", heap)

# Get the smallest element (peek, without removing)
smallest = heap[0]
print("Smallest element (peek):", smallest)

# Remove the smallest element
removed = heapq.heappop(heap)
print("Removed smallest element:", removed)
print("Heap after removing the smallest element:", heap)

# Add more elements
heapq.heappush(heap, 7)
heapq.heappush(heap, 2)
print("Heap after adding more elements:", heap)

# Get the three smallest elements (without removing them)
three_smallest = heapq.nsmallest(3, heap)
print("Three smallest elements:", three_smallest)

# Replace the smallest element with a new value (removes and adds in one operation)
heapq.heapreplace(heap, 7)
print("Heap after replacing the smallest element with 7:", heap)

# Remove all elements one by one
while heap:
    print("Removed:", heapq.heappop(heap))
