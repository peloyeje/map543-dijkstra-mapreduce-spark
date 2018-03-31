INPUT_FILE="$1"
PARAM="$2"

init() {
  TMP_DIR="$(pwd)/tmp/"
  # Create tmp directory
  if [ ! -d "$TMP_DIR" ]
  then
    mkdir -p "$TMP_DIR"
  fi
  if [ ! -f "$INPUT_FILE" ]
  then
    echo "Input file not found !"
  fi
}

launch_job() {
  TMP_FILENAME="output.txt"
  SUM_DISTANCES=0
  TOTAL_NODES=`cat "$INPUT_FILE" | wc -l`

  # Iteratively run mapreduce jobs until all possible paths are found
  for ((i=1; i>0; i++)); do
    echo "Starting iteration $i ..."

    DIST=0
    PAIR=$((i%2))
    TMP_FILE="$TMP_DIR$TMP_FILENAME$PAIR"

    # MapReduce job emulation
    cat "$INPUT_FILE" | ./mapper.py | sort -k1n | ./reducer.py > "$TMP_FILE"
    # Distance computation
    while read num
    do
      DIST=$((DIST + num))
    done <<< "$(cat "$TMP_FILE" | cut -d$'\t' -f2)"
    echo "Sum : $DIST"

    if [ "$DIST" -ge "$SUM_DISTANCES" ] &&  [ ! "$SUM_DISTANCES" -eq 0 ]
    then
      echo "Convergence criterion met !"
      break
    fi

    SUM_DISTANCES=$DIST
    INPUT_FILE="$TMP_FILE"
  done

  # Move final result file to current directory
  mv "$TMP_FILE" ./result.txt
  # Display the results
  if [ "$PARAM" == "-v" ]
  then
    echo "\n\n-----\n\n"
    cat ./result.txt | cut -d$'\t' -f1,2,4
  fi
  # Clear temporary files
  rm -rf "$TMP_DIR"
}

init
launch_job
