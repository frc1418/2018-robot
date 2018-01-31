# 2018 Robot Code
**Robot Code** | [Dashboard](https://github.com/frc1418/2018-dashboard) | [Vision](https://github.com/frc1418/2018-vision)

[![Build Status](https://travis-ci.com/frc1418/2018-robot.svg?token=xpnQFTGBHababzyAzqKV&branch=master)](https://travis-ci.com/frc1418/2018-robot)

> Code for Team 1418's 2018 competition robot.

## Robot code features
TODO

## Deploying onto the robot
The robot code is written in Python, so to run it you must install
[pyfrc](https://github.com/robotpy/pyfrc) onto the robot.

With the pyfrc library installed, you can deploy the code onto the robot
by running robot.py with the following argument:

	python3 robot.py deploy

This will run the unit tests and upload the code to the robot of your
choice.

## Testing/Simulation
The robot code has full integration with pyfrc. Make sure you have pyfrc
installed, and then you can use the various simulation/testing options
of the code by running robot.py directly.

    python3 robot.py sim

## Setting up `git` hooks:

`git` hooks change the process of committing by adding processes before or after the process of committing. After cloning, you should run

		./setup.sh

This will set up hooks to run tests before committing to help avoid easy-to-fix errors in the code.

## File Structure

    robot/
    	The robot code lives here.
        automations/
            Several automatic scripts for performing common functions.
        autonomous/
            Autonomous modes.
        common/
            New robotpy components.
        components/
            Abstractions for major robot systems.
	tests/
		py.test-based unit tests that test the code and can be run via pyfrc.

## Authors
* [Erik Boesen](https://github.com/ErikBoesen)

## Licensing
In-season, use of this software is restricted by the FRC rules. After the season ends, the [MIT License](LICENSE) applies instead.
