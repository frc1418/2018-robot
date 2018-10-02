# 2018 Robot Code
**Robot Code** | [Dashboard](https://github.com/frc1418/2018-dashboard) | [Vision](https://github.com/frc1418/2018-vision)

[![Build Status](https://travis-ci.com/frc1418/2018-robot.svg?token=xpnQFTGBHababzyAzqKV&branch=master)](https://travis-ci.com/frc1418/2018-robot)

> Code for Team 1418's 2018 competition robot, Panthera.

## Robot code features
* *Modular Autonomous:* Through our [dashboard](https://github.com/frc1418/2018-dashboard), drivers can select individual components of an autonomous mode. Or, they can select from several premade modes which inherit from modular with various preexisting configurations. "Optimum autonomous" may also be selected, which will choose the best target in which to score based on decisions made immediately after receiving plate ownership data from the FMS.
* *Autonomous Replay:* In addition to hard-coded modular paths, the autonomous code has a replay feature, which records joystick input and stores that data in a JSON file. This way, a driver can drive the robot in the desired path for autonomous, and it will use that same route when selected in autonomous. Voltage data is recorded alongside joystick input, and that data is used to scale output voltages during replay to prevent speed fluctuation caused by voltage variation.
* *Balancing system:* In order to prevent tipping, the robot constantly monitors its rotation in the pitch axis through our NavX, and in the event of an apparent tip, the drivetrain will spin in the opposite direction to pull the robot back down to the ground. Motor speeds will be scaled to prevent overshooting.

## Lessons Learned
We had fun with this year's robot and in our competitions using it. Each and every member of our team grew in their skillset and life experience during our 2018 season, and we [performed well in competition](http://1418.team/robot/2018). However, to quote pragmatist and American educational philosopher John Dewey:

> Failure is instructive. The person who really thinks learns quite as much from his failures as from his successes.

In accordance with this precept, here are several mistakes we made this year, which we will work to next year not make again.
* We should not have relied on dead-reckoning autonomous. In order to quickly get an autonomous mode up and running for demonstration, we used simple time and speed based dead-reckoning control to score during autonomous. This worked okay, but we quickly built up a reliance on using dead-reckoning. This fact capped our accuracy in autonomous mode: though we installed encoders on our robot and worked on motion profiling code, we ended up never tuning the system because doing so would require abandoning all the hard work we'd already done on our dead-reckoning system. Not putting substantial effort into developing a viable motion profiling system prevented us from doing as well as we could have done during autonomous mode and in competition.
* We should have made our autonomous even more modular. When we arrived at competition we realized we had neglected to support not crossing the field to score if neither goal ownership was on the robot's current side. This led to a conflict with another team's autonomous mode, nearly losing us a match. In the future, we should create modular presets for every situation we could possibly require (and, in our modular logic, support every chain of actions which could be taken).

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
* [Erik Boesen](https://github.com/ErikBoesen), Programming Captain
* [Andrew Lester](https://github.com/AndrewLester)
* [Joe Carpenter](https://github.com/JosephCarpenter)

Special thanks goes to [Tim Winters](https://github.com/Twinters007), former 1418 Programming Captain, who tirelessly worked as a mentor to help us reach new heights with this year's robot code.

## Licensing
In-season, use of this software is restricted by the FRC rules. After the season ends, the [MIT License](LICENSE) applies instead.
