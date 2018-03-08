# Panthera Autonomous Modes
**Name** | **Description**
--------:|:---------------
Charge **(DEFAULT)** | Cross the autonomous baseline.
OptimumNone[Left/Right] | Score on this side's scale or this side's switch if owned.
OptimumSwitch[Left/Right] | Score on this side's scale or this side's switch if owned. Otherwise, score in opposite side switch.
OptimumScale[Left/Right] | Score on this side's scale or this side's switch if owned. Otherwise, score in opposite side scale.
Switch[Left/Middle/Right] | Score in owned side of switch from the specified starting position.
Switch[Left/Right] | Score in owned side of scale from the specified starting position.
Replay | Play back a JSON-formatted autonomous recording. Recording name can be selected on the dashboard and is stored in `/autonomous/replay/source`.
