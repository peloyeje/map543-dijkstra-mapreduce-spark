#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.strip().split('\t')

    node = line[0]
    distance = line[1]
    # Set neighbours variable only if the node has some
    neighbours = line[2] if len(line) > 2 and line[2] != "0" else 0
    # Propagate computed path at previous step, or set beginning of path
    path = line[3] if len(line) == 4 else node

    try:
        distance = int(distance)
    except:
        # Skip node
        continue

    # Print complete node to keep the graph structure for future iterations
    print '%s\t%s\t%s\t%s' % (node, distance, neighbours, path)

    # If the node has no childs, there is nothing left to do.
    if neighbours:
        neighbours = neighbours.strip().split(',')

        # For each neighbor, print its updated distance to the source node
        for neighbour in neighbours:
            child_node, child_distance = neighbour.strip().split(':', 1)

            try:
                child_distance = int(child_distance)
            except:
                continue

            child_distance += distance
            child_path = '{}>{}'.format(path, str(child_node))

            print '%s\t%s\t%s' % (child_node, child_distance, child_path)
