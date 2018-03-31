# HDFS input
INPUT_DIR="$1"
OUTPUT_DIR="$2"
MAPPER_FILE="$3"
REDUCER_FILE="$4"
ITERATIONS="$5"

init() {
  TMP_DIR="$(pwd)/tmp/"
  # Create tmp directory
  if [ ! -d "$TMP_DIR" ]
  then
    mkdir -p "$TMP_DIR"
  fi
}

launch_job() {
  TMP_FILENAME="output.txt"
  SUM_DISTANCES=0

  # Iteratively run mapreduce jobs until all possible paths are found
  for ((i=1; i>0; i++)); do
    if [ ! -z $ITERATIONS ] && [ $i -gt $ITERATIONS ]
    then
      echo "Maximum number of iterations reached. Stopping ..."
      break
    fi

    echo "Starting iteration $i ..."

    DIST=0
    # MapReduce job
    hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
    -D mapreduce.partition.keycomparator.options=-n \
    -input "$INPUT_DIR" -output "$OUTPUT_DIR" \
    -file "$MAPPER_FILE" -mapper "$MAPPER_FILE" \
    -file "$REDUCER_FILE" -reducer "$REDUCER_FILE"

    # Distance computation
    TMP_FILE="$TMP_DIR$TMP_FILENAME"
    hdfs dfs -cat "$OUTPUT_DIR"/* > "$TMP_FILE"
    while read num
    do
      DIST=$((DIST + num))
    done <<< "$(cat "$TMP_FILE" | cut -d$'\t' -f2)"
    echo "Sum : $DIST"

    if [ "$DIST" -ge "$SUM_DISTANCES" ] && [ ! "$SUM_DISTANCES" -eq 0 ]
    then
      echo "End of convergence !"
      break
    fi

    SUM_DISTANCES=$DIST
    # Move reducer output into input directory to prepare the next job
    hdfs dfs -rm -r "$INPUT_DIR"/*
    hdfs dfs -mv "$OUTPUT_DIR"/* "$INPUT_DIR"
    hdfs dfs -rm -r -f "$OUTPUT_DIR"
  done

  # Move final result file to current directory
  hdfs dfs -cat "$OUTPUT_DIR"/* | sort -n > ./result.txt

  # Clear temporary files
  rm -rf "$TMP_DIR"
}

init
launch_job
