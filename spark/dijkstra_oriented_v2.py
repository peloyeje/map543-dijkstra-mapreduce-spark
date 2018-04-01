import time

import pyspark

conf = pyspark.SparkConf().setAppName("Dijkstra").set("spark.dynamicAllocation.enabled", "false")
sc = pyspark.SparkContext(conf=conf)
log4jLogger = sc._jvm.org.apache.log4j
logger = log4jLogger.LogManager.getLogger(__name__)


# helper functions
#
#
def read_generated_graph_line(line):
    line = line.strip().split("\t")
    if len(line) == 2:
        return
    elif len(line) == 3:
        origin = line[0]
        neighbours = line[2]
        try:
            return [(origin, (pair.split(":")[0].strip(), int(pair.split(":")[1].strip())))
                    for pair in neighbours.split(",")]
        except IndexError:
            raise RuntimeError("file not well formatted")
    else:
        return


def shortest_path_to_point(x, y):
    """ this function is a reduce function that computes the shortest path to a certain point (the key)"""

    if x["weight_of_path"] <= y["weight_of_path"]:
        res = {"weight_of_path": x["weight_of_path"],
               "path": x["path"]}
    else:
        res = {"weight_of_path": y["weight_of_path"],
               "path": y["path"]}
    return res


def compute_path(x):
    """computes the path resulting from a join from existing paths and the directions rdd"""

    # x is the result of the join operation
    # the join should be in format
    # (origin, ((weight_to_origin, path_to_origin, paths_visited_to_origin), (destination, weight_to_destination)))
    return (x[1][1][0], {
                         "weight_of_path": x[1][0]["weight_of_path"] + x[1][1][1],
                         "path": x[1][0]["path"] + [x[0]]
    })


def get_txt(path):
    res = str(path[0])
    res += " : " + ">".join(path[1]["path"])
    res += " for weight " + str(path[1]["weight_of_path"])
    return res


# Initialisation
#
#
# a file named graph.txt must be provided in the --file option of spark submit
n_part = 6
directions = sc.textFile("hdfs:///user/hadoop/graph_100.txt").filter(lambda x: x != "").flatMap(read_generated_graph_line)
begin = "1"
shortest_paths = sc.parallelize([(begin, {"weight_of_path": 0, "path": []})]).partitionBy(n_part)
final_paths = sc.emptyRDD()
early_stop = 30
continue_criteria = True
points_to_drop = sc.broadcast(set())


# Algo
#
#
i = 0
while continue_criteria:
    print("##### iteration {} ######".format(i))
    print("size directions : {}".format(directions.count()))
    print("size paths {}".format(shortest_paths.count()))

    time_0 = time.time()
    time_1 = time.time()

    # finding all the paths connected with the already visited points
    new_paths = shortest_paths.join(directions, n_part).map(compute_path).cache()
    print("join result size : {}".format(new_paths.count()))
    print("join time : {}".format(time.time() - time_0))
    time_0 = time.time()
    try:
        # value of the minimum path to one of those points reached at step n+1
        min_new_paths = sc.broadcast(new_paths.map(lambda x: x[1]["weight_of_path"]).min())
        print("min time = {}".format(time.time() - time_0))
        time_0 = time.time()

        # we can now abandon all the paths reached at step n with a smaller path than the min calculated above
        # (these paths cannot be improoved further)
        points_to_drop = sc.broadcast(set(shortest_paths.filter(
            lambda x: x[1]["weight_of_path"] < min_new_paths.value).keys().collect()) | points_to_drop.value)
        print("find points to drop : {}".format(time.time() - time_0))
    except ValueError:
        # if no new paths are detected:
        min_new_paths = sc.broadcast(float("inf"))

    # we can now combine the new paths with the reamining old paths
    time_0 = time.time()
    shortest_paths = new_paths.union(shortest_paths).reduceByKey(shortest_path_to_point)
    final_paths = final_paths.union(shortest_paths.filter(lambda x: x[0] in points_to_drop.value))
    shortest_paths = shortest_paths.filter(lambda x: x[0] not in points_to_drop.value)
    shortest_paths.cache()
    shortest_paths.collect()
    print("reduce by key : {}".format(time.time() - time_0))

    # we can also drop all the directions going from and to the droped points in order to increase speed of the join
    time_0 = time.time()
    directions = directions.filter(lambda x: x[0] not in points_to_drop.value and x[1][0] not in points_to_drop.value)
    directions.cache()
    # stopping criteria
    i += 1

    continue_criteria = min_new_paths.value != float("inf") and i < early_stop
    print("filter directions : {}".format(time.time() - time_0))
    print("total_time : {} \n\n\n".format(time.time() - time_1))

final_paths = final_paths.union(shortest_paths)


# add save for final_paths
final_paths.map(get_txt).coalesce(n_part).saveAsTextFile("results/")
