#!/usr/local/bin/python3
import argparse
import random

## DEFAULT CONSTANTS
# Total number of nodes in the generated graph
TOTAL_NODES = 100
# Maximum number of outgoing directed links from each node
MAX_OUTBOUND_LINKS = 10
# Maximum distance/weight on the link of each node
MAX_WEIGHT = 20

## CLI ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('total_nodes', type=int, nargs='?', default=TOTAL_NODES,
    help="Total number of nodes in the generated graph")
parser.add_argument('max_links', type=int, nargs='?', default=MAX_OUTBOUND_LINKS,
    help="Maximum number of outgoing directed links from each node")
parser.add_argument('max_weight', type=int, nargs='?', default=MAX_WEIGHT,
    help="Maximum distance/weight on the link of each nodee")
args = parser.parse_args()

nodes = range(1, args.total_nodes+1)

for point in nodes:
    # Randomly select a number of outgoing directed links for this node
    nb_neighbors = random.randint(1, args.max_links)
    # Randomly select k linked nodes in the node population
    neighbors = random.sample(nodes, nb_neighbors)
    for neighbor in neighbors:
        # Choose a weight for each link
        distance = random.randint(1, args.max_weight)
        # Print the line
        output = [point, neighbor, distance]
        print('\t'.join((str(x) for x in output)))
