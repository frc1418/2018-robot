import wpilib
from magicbot import will_reset_to
from magicbot import tunable


class Arm:
    """
    Operate robot arm (all components).
    """
    elevator: wpilib.Victor
    forearm: wpilib.DoubleSolenoid
    claw: wpilib.DoubleSolenoid
    intake: wpilib.Spark

    _elevator_speed = will_reset_to(0)
    _intake_speed = will_reset_to(0)

    motion_constant = tunable(0.6)
    extended = tunable(False)

    @property
    def is_open(self):
        """
        Is claw open?

        :return: Are claw pistons extended to open the arm?
        """
        return self.claw.get() == wpilib.DoubleSolenoid.Value.kForward

    @property
    def is_closed(self):
        """
        Is claw closed?

        :return: Are claw pistons retracted to close the arm?
        """
        return self.claw.get() == wpilib.DoubleSolenoid.Value.kReverse

    @property
    def is_extended(self):
        """
        Is forearm extended?

        :return: Is forearm piston extended so as to do the same to the arm?
        """
        return self.forearm.get() == wpilib.DoubleSolenoid.Value.kForward

    @property
    def is_retracted(self):
        """
        Is forearm retracted?

        :return: Is forearm piston retracted so as to do the same to the arm?
        """
        return self.forearm.get() == wpilib.DoubleSolenoid.Value.kReverse

    def move(self, speed: float):
        """
        Set the motor speed of claw elbow.

        :param speed: The requested speed, between -1 and 1.
        """
        self._elevator_speed = speed

    def up(self):
        """
        Move arm upward.

        Used when controlling arm through buttons.
        """
        self._elevator_speed = 1 * self.motion_constant

    def down(self):
        """
        Move arm downward.

        Used when controlling arm through buttons.
        """
        self._elevator_speed = -1 * self.motion_constant

    def extend(self):
        """
        Extend forearm.
        """
        self.forearm.set(wpilib.DoubleSolenoid.Value.kForward)

    def retract(self):
        """
        Retract forearm.
        """
        self.forearm.set(wpilib.DoubleSolenoid.Value.kReverse)

    def actuate_forearm(self):
        """
        Extend or retract forearm based on current position.
        """
        if self.is_retracted:
            self.extend()
        else:
            self.retract()

        self.extended = self.is_extended

    def grip(self):
        """
        Grip cube in claw.
        """
        self.claw.set(wpilib.DoubleSolenoid.Value.kReverse)

    def release(self):
        """
        Release cube from claw.
        """
        self.claw.set(wpilib.DoubleSolenoid.Value.kForward)

    def actuate_claw(self):
        """
        Grip or release cube based on current state.
        """
        if self.is_open:
            self.grip()
        else:
            self.release()

    def spin_in(self):
        """
        Spin the intake wheels inwards.
        """
        self._intake_speed = -1

    def spin_out(self):
        """
        Spin the intake wheels outwards.
        """
        self._intake_speed = 1

    def execute(self):
        """
        Run elevator motors.
        """
        self.elevator.set(-self._elevator_speed)
        self.intake.set(self._intake_speed)
