#!/usr/bin/python

import sys

current_dist = None
current_node = None
current_path = None

for line in sys.stdin:
    line = line.strip().split('\t')
    if len(line)==4:
        node = line[0]
        dist= line[1]
        neighbours = line[2]
        path = line[3]
    if len(line)==3:
        node = line[0]
        dist = line[1]
        path = line[2]

    try:
        dist = int(dist)
    except:
        continue

    if current_node == node:
        if dist < current_dist:
            current_dist = dist
            current_path = path
    else:
        if current_node:
            print '%s\t%s\t%s\t%s' % (current_node, current_dist, neighbours, current_path)
        current_node = node
        current_dist = dist
        current_path = path

if current_node == node:
    print '%s\t%s\t%s\t%s' % (current_node, current_dist, neighbours, current_path)
