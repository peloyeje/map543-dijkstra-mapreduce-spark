#!/usr/local/bin/python3

import sys
import random
import argparse

## DEFAULT CONSTANTS
# Maximum distance/weight on the link of each node
MAX_WEIGHT = 30

## CLI ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('max_weight', type=int, nargs='?', default=MAX_WEIGHT,
    help="Maximum distance/weight on the link of each node")
args = parser.parse_args()

current_node = None
current_neighbors = []
current_count = 0

def print_line(node, neighbors, first=False):
    # Sort the (neighbor, weight) tuple by node id
    neighbors = sorted(neighbors, key=lambda x: x[0])
    # Format the tuples as neighbor:weight strings
    directions = ['{}:{}'.format(neigh, dist) for (neigh, dist) in neighbors]
    # Set initial maximum distance to all nodes except the origin
    distance = 0 if first else args.max_weight*100
    print('{}\t{}\t{}'.format(node, distance, ','.join(directions)))

for line in sys.stdin:
    items = line.strip().split(' ', 1)

    try:
        node, neighbor = [int(x) for x in items]
        weight = random.randint(1, args.max_weight)
    except:
        # Skip line
        raise
    print
    if node == current_node:
        current_neighbors.append((neighbor, weight))
    else:
        if current_node:
            print_line(current_node, current_neighbors, first=(current_count == 1))
        current_node = node
        current_neighbors = [(neighbor, weight)]
        current_count += 1

# Clear the buffer and print the remaining node data
print_line(current_node, current_neighbors)
