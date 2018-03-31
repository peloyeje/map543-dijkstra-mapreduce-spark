## Dijkstra algorithm

### Overview

### Data

### MapReduce (Hadoop Streaming)

#### In a local environment

##### Structure of an iteration

```
cd mapreduce
cat my-preprocessed-graph.txt | ./mapper.py | sort -k1n | ./reducer.py > step1.txt
```

##### Bash script to automate iterations

```
./launch_chained_job.sh <my-graph-file> [-v]
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
