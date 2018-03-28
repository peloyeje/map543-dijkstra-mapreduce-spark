#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.strip().split('\t')
    node = line[0]
    distance = int(line[1])
    neighbours = line[2]
    if len(line) > 3:
        path = line[3]
    else:
        path = node
    print '%s\t%s\t%s\t%s' % (node,distance,neighbours,node)
    neighbours = neighbours.strip().split(',')
    for neighbour in neighbours:
        pair = neighbour.strip().split(':')
        child_node = pair[0]
        dist = int(pair[1])
        child_dist = distance + dist
        child_path = path + '->' + str(child_node)
        print '%s\t%s\t%s' % (child_node, child_dist, child_path)
