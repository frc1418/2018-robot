#!/usr/bin/env bash
set -e

# You should set the following environment variables:
#   $DEPLOY_START_NETWORK_PSK: Password/PSK of your current network
#   $DEPLOY_ROBOT_NETWORK_PSK: ...of your robot network

if ! [ "$(git status --porcelain)" = "" ]; then
    echo "Warning: You have uncommitted changes!"
fi

if [ "$DEPLOY_START_NETWORK_PSK" = "" ]; then
    echo "Warning: \$DEPLOY_START_NETWORK_PSK not set."
fi
if [ "$DEPLOY_ROBOT_NETWORK_PSK" = "" ]; then
    echo "Warning: \$DEPLOY_ROBOT_NETWORK_PSK not set."
fi

start_network=$(networksetup -getairportnetwork en0 | cut -d ' ' -f 4)
robot_network=1418

printf "Connecting to $robot_network... "
if ! [ "$(networksetup -setairportnetwork en0 $robot_network $DEPLOY_ROBOT_NETWORK_PSK)" = "" ]; then
    exit 1
else echo "👍"; fi
python3 robot/robot.py deploy
printf "Reconnecting to $start_network... "
if ! [ "$(networksetup -setairportnetwork en0 $start_network $DEPLOY_START_NETWORK_PSK)" = "" ]; then
    exit 1
else echo "👍"; fi
