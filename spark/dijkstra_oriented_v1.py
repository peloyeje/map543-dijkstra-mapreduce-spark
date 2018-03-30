from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("dijkstra").getOrCreate()
sc = spark.sparkContext


# helper functions
#
#
def read_generated_graph(path_to_file):
    """ reads a graph computed by the graph_generator.py program"""

    res = sc.textFile(path_to_file).map(lambda x: (x.split("\t")[0], (x.split("\t")[1], int(x.split("\t")[2]))))
    return res


# connections are denoted (origin, (end, weight))
# paths to a point are denoted (point, (weight, path, incoming_points_tested


def compute_path(x):
    """computes the path resulting from a join from existing paths and the directions rdd"""

    # x is the result of the join operation
    # the join should be in format
    # (origin, ((weight_to_origin, path_to_origin, paths_visited_to_origin), (destination, weight_to_destination)))
    return x[1][1][0], (x[1][0][0] + x[1][1][1], x[1][0][1] + [x[0]], {x[0]})


def shortest_path_to_point(x, y):
    """ this function is a reduce function that computes the shortest path to a certain point (the key)"""

    if x[0] <= y[0]:
        res = (x[0], x[1], x[2] | y[2])
    else:
        res = (y[0], y[1], x[2] | y[2])
    return res


# initialisation
#
#
directions = read_generated_graph("file:///graph.txt")
begin, objective = directions.keys().takeSample(False, 2)
paths_to_objective = set(directions.map(lambda x: (x[1][0], x[0])).filter(lambda x: x[0] == objective).values().collect())
shortest_paths = sc.parallelize([(begin, (0, [], set()))])
path_found = []
early_stop = 15
i = 0

# algo
#
#
while True:
    # stopping criteria
    i += 1
    print(i)
    if i > early_stop:
        break
    path_found = shortest_paths.filter(lambda x: x[0] == objective).collect()
    if path_found != [] and path_found[0][1][2] == paths_to_objective:
        break

    # computing paths
    shortest_paths = shortest_paths.join(directions).map(compute_path).union(shortest_paths)
    shortest_paths = shortest_paths.reduceByKey(shortest_path_to_point)

if path_found:
    print("##### algo reached end #####")
    print(path_found)
