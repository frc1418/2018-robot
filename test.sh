#!/usr/bin/env bash
set -e

python3 robot/robot.py test
pycodestyle . --ignore=E501
