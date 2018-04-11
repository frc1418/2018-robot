# 2018 Robot Code
**Robot Code** | [Dashboard](https://github.com/frc1418/2018-dashboard) | [Vision](https://github.com/frc1418/2018-vision)

[![Build Status](https://travis-ci.com/frc1418/2018-robot.svg?token=xpnQFTGBHababzyAzqKV&branch=master)](https://travis-ci.com/frc1418/2018-robot)

> Code for Team 1418's 2018 competition robot, Panthera.

## Robot code features
#### Modular Autonomous
You can select which autonomous module you want to use depending on your placement during a game, with left, middle, and right versions of scoring on the switch and scale on both sides. You can also select an optimal autonomous mode, which decides automatically which path to use depending on position and priority.
#### Replay system
In addition to hard-coded modular paths, the autonomous code has a replay feature, which records joystick input and saves it as an autonomous path as a JSON file. This way, a driver can drive the robot in the desired path for autonomous, and it will use that same route when selected in autonomous. It measures the voltage that the battery is at when recording, and alters the speed when replaying according to the voltage factor.
#### Balancing system
In order to prevent any tipping or imbalance issues, the robot code equips the robot with a rebalancing system. It counteracts any leaning or instability the robot may have.

## Deploying onto the robot
Before deploying, you must [install robotpy](http://robotpy.readthedocs.io/en/stable/install/robot.html#install-robotpy) on your robot.

You may then deploy code at any time:

	python3 robot.py deploy

During development of this year's robot code, we created a Bash script `deploy.sh` to automate some tasks related to code deploy. The script's featureset swelled significantly, and we elected to spin the tool off into a season-independent command line tool. You can find that tool, `dep`, [here](https://github.com/frc1418/dep). We recommend that you make use of it to simplify your deploy process and remove pesky steps like changing your WiFi network.

## Testing/Simulation
You may run the `pyfrc` simulator to test this code thus:

    python3 robot.py sim

## Controls
We use three total joysticks to control the robot:

* 2 x **Logitech Attack 3** (`joystick_left` and `joystick_right`)
* 1 x **Logitech Extreme 3D Pro** (`joystick_alt`)

<img src="res/ATK3.png" height="600"><img src="res/X3D.png" height="600">

## Setting up `git` hooks:

`git` hooks change the process of committing by adding processes before or after the process of committing. After cloning, you should run

	./setup.sh

This will set up hooks to run tests before committing to help avoid easy-to-fix errors in the code.

## File Structure

    robot/
    	The robot code lives here.
        automations/
            Automatic scripts for performing common functions.
        autonomous/
            Autonomous modes.
        common/
            New robotpy components.
        components/
            Abstractions for major robot systems.
        controllers/
            Software implementations not corresponding to physical robot components.
	tests/
		py.test-based unit tests that test the code and can be run via pyfrc.

## Authors
* [Erik Boesen](https://github.com/ErikBoesen)

## Licensing
In-season, use of this software is restricted by the FRC rules. After the season ends, the [MIT License](LICENSE) applies instead.
