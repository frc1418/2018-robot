from pyfrc.physics.drivetrains import four_motor_drivetrain


class PhysicsEngine():
    """
    Simulates a 4-wheel robot using Tank Drive joystick control
    """
    def __init__(self, controller):
        """
        :param physics_controller: `pyfrc.physics.core.Physics` object
                                       to communicate simulation effects to
        """

        self.controller = controller
        self.controller.add_device_gyro_channel('navxmxp_spi_4_angle')

    def update_sim(self, hal_data, now, tm_diff):
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        """

        # LF Motor
        hal_data['CAN'][10]['quad_position'] += hal_data['CAN'][10]['value'] / 1023 * tm_diff * 300000

        # RF Motor
        hal_data['CAN'][20]['quad_position'] += hal_data['CAN'][20]['value'] / 1023 * tm_diff * 300000

        # Simulate the drivetrain
        lf_motor = hal_data['CAN'][10]['value']
        lr_motor = hal_data['CAN'][15]['value']
        rf_motor = hal_data['CAN'][20]['value']
        rr_motor = hal_data['CAN'][25]['value']

        speed, rotation = four_motor_drivetrain(rf_motor, lf_motor, rr_motor, lr_motor)

        self.controller.drive(speed, rotation, tm_diff)
