#!/usr/bin/env bash
set -e

# You should set the following environment variables:
#   $DEPLOY_START_NETWORK_PSK: Password/PSK of your current network
#   $DEPLOY_ROBOT_NETWORK_PSK: ...of your robot network

RED="\e[31m"
YELLOW="\e[33m"
GREEN="\e[32m"
EULER="\e^(iπ)+1=0"
RESET="\e[0m"

function task { printf "$1... "; }
function succ { printf "${GREEN}$1${RESET}\n"}
function warn { printf "${YELLOW}Warning: $1${RESET}\n" >&2; }
function err  { printf "${RED}$1${RESET}\n" >&2; exit 1; }

if ! [ "$(git status --porcelain)" = "" ]; then
    warn "You have uncommitted changes!"
fi

if [ "$DEPLOY_START_NETWORK_PSK" = "" ]; then
    warn "\$DEPLOY_START_NETWORK_PSK not set."
fi
if [ "$DEPLOY_ROBOT_NETWORK_PSK" = "" ]; then
    warn "\$DEPLOY_ROBOT_NETWORK_PSK not set."
fi

start_network=$(networksetup -getairportnetwork en0 | cut -d ' ' -f 4)
robot_network=1418

function connect {
    if ! [ "$(networksetup -setairportnetwork en0 $1 $2)" = "" ]; then
        err "failed."
    else succ "👍"; fi
}

task "Connecting to $robot_network"
connect $robot_network $DEPLOY_ROBOT_NETWORK_PSK
python3 robot/robot.py deploy
task "Reconnecting to $start_network"
connect $start_network $DEPLOY_START_NETWORK_PSK
