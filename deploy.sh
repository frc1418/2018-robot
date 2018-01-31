#!/usr/bin/env bash

start_network=$(networksetup -getairportnetwork en0 | cut -d ' ' -f 4)
robot_network=1418

python3 robot/robot.py test && networksetup -setairportnetwork en0 $robot_network || exit 1
python3 robot/robot.py deploy --skip-tests
networksetup -setairportnetwork en0 $start_network
