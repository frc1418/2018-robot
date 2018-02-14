#!/usr/bin/env bash

start_network=$(networksetup -getairportnetwork en0 | cut -d ' ' -f 4)
robot_network=1418

echo "Connecting to $robot_network, with PSK hash beginning $(shasum <<< "$DEPLOY_ROBOT_NETWORK_PSK" | cut -c -8)..."
networksetup -setairportnetwork en0 $robot_network $DEPLOY_ROBOT_NETWORK_PSK
python3 robot/robot.py deploy
echo "Reconnecting to $start_network, with PSK hash beginning $(shasum <<< "$DEPLOY_START_NETWORK_PSK" | cut -c -8)..."
networksetup -setairportnetwork en0 $start_network $DEPLOY_START_NETWORK_PSK
