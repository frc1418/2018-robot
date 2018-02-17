#!/usr/bin/env bash
set -e

# You should set the following environment variables:
#   $DEPLOY_START_NETWORK_PSK: Password/PSK of your current network
#   $DEPLOY_ROBOT_NETWORK_PSK: ...of your robot network

RED="\e[31m"
YELLOW="\e[33m"
GREEN="\e[32m"
RESET="\e[0m"

if ! [ "$(git status --porcelain)" = "" ]; then
    echo -e "${YELLOW}Warning: You have uncommitted changes!${RESET}"
fi

if [ "$DEPLOY_START_NETWORK_PSK" = "" ]; then
    echo -e "${YELLOW}Warning: \$DEPLOY_START_NETWORK_PSK not set.${RESET}"
fi
if [ "$DEPLOY_ROBOT_NETWORK_PSK" = "" ]; then
    echo -e "${YELLOW}Warning: \$DEPLOY_ROBOT_NETWORK_PSK not set.${RESET}"
fi

start_network=$(networksetup -getairportnetwork en0 | cut -d ' ' -f 4)
robot_network=1418

function connect {
    if ! [ "$(networksetup -setairportnetwork en0 $1 $2)" = "" ]; then
        echo -e "${RED}failed.${RESET}"
        exit 1
    else echo "👍"; fi
}

printf "Connecting to $robot_network... "
connect $robot_network $DEPLOY_ROBOT_NETWORK_PSK
python3 robot/robot.py deploy
printf "Reconnecting to $start_network... "
connect $start_network $DEPLOY_START_NETWORK_PSK
