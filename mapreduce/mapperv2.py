#!/usr/local/bin/python3

import sys

for line in sys.stdin:
    line = line.strip().split('\t')

    node = line[0]
    distance = line[1]
    neighbours = line[2] if len(line) > 2 and line[2] != "0" else 0
    path = line[3] if len(line) == 4 else node

    try:
        distance = int(distance)
    except:
        continue

    # Print complete node
    print('{}\t{}\t{}\t{}'.format(node, distance, neighbours, node))

    if neighbours:
        neighbours = neighbours.strip().split(',')

        for neighbour in neighbours:
            child_node, child_distance = neighbour.strip().split(':', 1)

            try:
                child_distance = int(child_distance)
            except:
                continue

            child_distance += distance
            child_path = '{}>{}'.format(path, str(child_node))

            print('{}\t{}\t{}'.format(child_node, child_distance, child_path))
