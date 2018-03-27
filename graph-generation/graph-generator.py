#!/usr/local/bin/python3

import random

# Total number of nodes in the generated graph
TOTAL_NODES = 100
# Maximum number of outgoing directed links from each node
MAX_OUTBOUND_LINKS = 10
# Maximum distance/weight on the link of each node
MAX_WEIGHT = 20

nodes = range(1, TOTAL_NODES+1)

for point in nodes:
    # Randomly select a number of outgoing directed links for this node
    nb_neighbors = random.randint(1, MAX_OUTBOUND_LINKS)
    # Randomly select k linked nodes in the node population
    neighbors = random.sample(nodes, nb_neighbors)
    for neighbor in neighbors:
        # Choose a weight for each link
        distance = random.randint(1, MAX_WEIGHT)
        # Print the line
        output = [point, neighbor, distance]
        print('\t'.join((str(x) for x in output)))
