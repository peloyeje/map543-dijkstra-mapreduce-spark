from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("dikjstra").getOrCreate()
sc = spark.sparkContext


# helper functions
#
#
def read_generated_graph(path_to_file):
    """ reads a graph computed by the graph_generator.py program"""

    res = sc.textFile(path_to_file).map(lambda x: (x.split("\t")[0], (x.split("\t")[1], int(x.split("\t")[2]))))
    return res


def shortest_path_to_point(x, y):
    """ this function is a reduce function that computes the shortest path to a certain point (the key)"""

    if x["weight_of_path"] <= y["weight_of_path"]:
        res = {"weight_of_path": x["weight_of_path"],
               "path": x["path"],
               "explored_path": x["explored_path"] | y["explored_path"]}
    else:
        res = {"weight_of_path": y["weight_of_path"],
               "path": y["path"],
               "explored_path": x["explored_path"] | y["explored_path"]}
    return res


def compute_path(x):
    """computes the path resulting from a join from existing paths and the directions rdd"""

    # x is the result of the join operation
    # the join should be in format
    # (origin, ((weight_to_origin, path_to_origin, paths_visited_to_origin), (destination, weight_to_destination)))
    return (x[1][1][0], {
                         "weight_of_path": x[1][0]["weight_of_path"] + x[1][1][1],
                         "path": x[1][0]["path"] + [x[0]],
                         "explored_path": {x[0]}
    })


# Initialisation
#
#
# a file named graph.txt must be provided in the --file option of spark submit
directions = read_generated_graph("file:///graph.txt")
begin, objective = directions.keys().takeSample(False, 2)
paths_to_objective = set(directions.map(lambda x: (x[1][0], x[0])).filter(lambda x: x[0] == objective).lookup(objective))
shortest_paths = sc.parallelize([(begin, {"weight_of_path": 0, "path": [], "explored_path": set()})])
early_stop = 15
continue_criteria = True
objective_reached = False
points_to_drop = sc.broadcast(set())
path_to_objective = []


# Algo
#
#
i = 0
while continue_criteria:

    # finding all the paths connected with the already visited points
    new_paths = shortest_paths.join(directions).map(compute_path)
    try:
        # value of the minimum path to one of those points reached at step n+1
        min_new_paths = sc.broadcast(new_paths.map(lambda x: x[1]["weight_of_path"]).min())

        # we can now abandon all the paths reached at step n with a smaller path than the min calculated above
        # (these paths cannot be improoved further)
        points_to_drop = sc.broadcast(set(shortest_paths.filter(
            lambda x: x[1]["weight_of_path"] < min_new_paths.value).keys().collect()) | points_to_drop.value)
    except ValueError:
        # if no new paths are detected:
        min_new_paths = sc.broadcast(float("inf"))

    # we can now combine the new paths with the reamining old paths
    shortest_paths = new_paths.union(shortest_paths).reduceByKey(shortest_path_to_point).filter(
        lambda x: x[0] not in points_to_drop.value)

    # we can also drop all the directions going from and to the droped points in order to increase speed of the join
    directions = directions.filter(lambda x: x[0] not in points_to_drop.value and x[1][0] not in points_to_drop.value)

    # stopping criteria
    early_stop_criteria = i < early_stop
    i += 1
    print(i)
    try:
        # replace by lookup on real machine when hash problem is resolved
        path_to_objective = shortest_paths.filter(lambda x: x[0] == objective).collect()
        objective_reached = (not path_to_objective[0][1]["weight_of_path"] <= min_new_paths.value
                             if path_to_objective != [] else False)
    except IndexError:
        early_stop_criteria = min_new_paths.value != float("inf")
        pass
    except KeyError:
        early_stop_criteria = min_new_paths.value != float("inf")
        pass

    continue_criteria = objective_reached and early_stop_criteria


# printing results
if objective_reached:
    print("##### shrotest path found #####")
    print(path_to_objective)
