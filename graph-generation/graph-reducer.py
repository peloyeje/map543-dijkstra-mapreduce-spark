#!/usr/local/bin/python3

import sys

current_node = None
current_neighbors = []

def print_line(node, neighbors):
    # Sort the (neighbor, weight) tuple by node id
    neighbors = sorted(neighbors, key=lambda x: x[0])
    # Format the tuples as neighbor:weight strings
    directions = ['{}:{}'.format(neigh, dist) for (neigh, dist) in neighbors]
    # Set initial maximum distance to all nodes except the origin
    distance = 0 if node == 1 else 10000
    print('{}\t{}\t{}'.format(node, distance, ','.join(directions)))

for line in sys.stdin:
    items = line.strip().split('\t', 2)

    try:
        if len(items) == 3:
            node, neighbor, weight = [int(x) for x in items]
        else:
            print_line(int(items[0]), [])
            continue
    except:
        # Skip line
        continue

    if node == current_node:
        current_neighbors.append((neighbor, weight))
    else:
        if current_node:
            print_line(current_node, current_neighbors)
        current_node = node
        current_neighbors = [(neighbor, weight)]

# Clear the buffer and print the remaining node data
print_line(current_node, current_neighbors)
