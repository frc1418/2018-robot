start_network=$(networksetup -getairportnetwork en0 | cut -d ' ' -f 4)
robot_network=1418

networksetup -setairportnetwork en0 $robot_network
python3 robot/robot.py deploy
networksetup -setairportnetwork en0 $start_network
