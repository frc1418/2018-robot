trap "exit 1" TERM
export TOP_PID=$$
python3 robot/robot.py test

print () {
    python3 tests/test_print.py $1;
    rc=$?; if [[ $rc != 0 ]]; then kill -s TERM $TOP_PID; fi;
}
export -f print
