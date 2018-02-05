import wpilib
from magicbot import will_reset_to


class Crane:
    """
    Operate robot arm (all components).
    """
    elevator: wpilib.Victor
    forearm: wpilib.DoubleSolenoid
    claw: wpilib.DoubleSolenoid

    _elevator_speed = will_reset_to(0)

    def move(self, speed: float):
        """
        Set the motor speed of claw elbow.

        :param speed: The requested speed, between -1 and 1.
        """
        self._elevator_speed = speed

    def extend_forearm(self):
        """
        Extend forearm.
        """
        self.forearm.set(2)

    def retract_forearm(self):
        """
        Retract forearm.
        """
        self.forearm.set(1)

    def actuate_forearm(self):
        """
        Extend or retract forearm based on current position.
        """
        # Switch between 1 and 2
        self.forearm.set(3 - self.forearm.get())

    def grip(self):
        """
        Grip cube in claw.
        """
        self.claw.set(1)

    def release(self):
        """
        Release cube from claw.
        """
        self.claw.set(2)

    def actuate_claw(self):
        """
        Grip or release cube based on current state.
        """
        # Switch between 1 and 2
        self.claw.set(3 - self.claw.get())

    def execute(self):
        """
        Run elevator motors.
        """
        self.elevator.set(self._elevator_speed)
