#!/usr/bin/env bash

function psk_hash {
    printf $(shasum <<< "$1" | cut -c -8)
}

start_network=$(networksetup -getairportnetwork en0 | cut -d ' ' -f 4)
robot_network=1418

echo "Connecting to $robot_network, with PSK hash beginning $(psk_hash $DEPLOY_ROBOT_NETWORK_PSK)..."
networksetup -setairportnetwork en0 $robot_network $DEPLOY_ROBOT_NETWORK_PSK
python3 robot/robot.py deploy
echo "Reconnecting to $start_network, with PSK hash beginning $(psk_hash $DEPLOY_START_NETWORK_PSK)..."
networksetup -setairportnetwork en0 $start_network $DEPLOY_START_NETWORK_PSK
