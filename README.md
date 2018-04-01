## Dijkstra algorithm

[MAP543 Database Management] Final project

**Authors**
- [Sami Mhirech](@samimhirech)
- [Jean-Eudes Peloye](@peloyeje)
- [Antoine Redier](@aredier)

### Overview

The Dijkstra algorithm is an algorithm that enables to find the shortest/lowest-cost path between two nodes in a graph. In its more common variant, it allows to compute a shortest path tree, i.e. the shortest paths to a source node for each node of the graph. Distance can be considered as the number of hops between nodes or as the sum of the weights/costs of the edges between nodes. It is a restricted application of the best-first search algorithm.

The  idea of the algorithm is to iteratively compute each graph node’s distance to the source node, and stop when all nodes have been visited. At each iteration, starting from the source node, each children distance to the selected node is updated with (parent distance + parent-child distance). The node selection is done according to the lowest distance to the previously selected node.

![Diagram of the Dijkstra’s shortest path algorithm](http://cs.smith.edu/~streinu/Teaching/Courses/274/Spring98/Projects/Philip/fp/dijkstra.jpg)

### Data

- twitter-formatted.txt : formatted Twitter graph data from the [SNAP Project](https://snap.stanford.edu/data/twitter_combined.txt.gz)

Generated graph data where nodes may not have outgoing vertices
- shallow-weighted-graph-1000.txt
- shallow-weighted-graph-10000.txt
- shallow-weighted-graph-100000.txt

Generated complete graph data
- weighted-graph-1000.txt
- weighted-graph-10000.txt
- weighted-graph-100000.txt

### MapReduce (Hadoop Streaming)

#### In a local environment

##### Structure of an iteration

```
cd mapreduce
cat my-preprocessed-graph.txt | ./mapper.py | sort -k1n | ./reducer.py > step1.txt
```

##### Bash script to automate iterations

```
./launch_local.sh <my-graph-file> [-v]
```

It performs unlimited iterations. Convergence is detected if the sum of distances between all nodes and the source node stops decreasing in iteration `n+1`

#### On a Hadoop cluster

##### Structure of an iteration

- Input folder : **input/**
  - Contains input graph or the reducer output of the last iteration
- Output folder : **output/**

```
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
-D mapreduce.partition.keycomparator.options=-n \
-input /user/hadoop/input -output /user/hadoop/output \
-file mapreduce/mapper.py -mapper mapreduce/mapper.py \
-file mapreduce/reducer.py -reducer mapreduce/reducer.py
```

##### Bash script to automate iterations

```
./launch_hadoop.sh <hdfs-input-path> <hdfs-output-path> <local-mapper-path> <local-reducer-path> [nb_iterations]
```
