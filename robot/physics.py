from pyfrc.physics.drivetrains import FourMotorDrivetrain
import pathfinder as pf
import math


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
        self.drivetrain = FourMotorDrivetrain(x_wheelbase=1.6, speed=7)
        self.encoder_ticks = 1440 / (0.5 * math.pi)
        self.left_encoder = 0
        self.right_encoder = 0

    def update_sim(self, hal_data, now, tm_diff):
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        """

<<<<<<< HEAD
=======
        try:
            self.rf_rotate_encoder += hal_data['analog'][2]['value'] * tm_diff * 20
            self.lf_rotate_encoder += hal_data['analog'][0]['value'] * tm_diff * 20

            self.rr_rotate_encoder %= 5
            self.rl_rotate_encoder %= 5
            self.fr_rotate_encoder %= 5
            self.fl_rotate_encoder %= 5

            hal_data['analog_in'][0]['avg_voltage'] = self.rr_rotate_encoder
            hal_data['analog_in'][2]['avg_voltage'] = self.rl_rotate_encoder
            hal_data['analog_in'][1]['avg_voltage'] = self.fr_rotate_encoder
            hal_data['analog_in'][3]['avg_voltage'] = self.fl_rotate_encoder
        except Exception:
            pass

        # LF Motor
        hal_data['CAN'][10]['quad_position'] += hal_data['CAN'][10]['value'] / 1023 * tm_diff * 300000

        # RF Motor
        hal_data['CAN'][20]['quad_position'] += hal_data['CAN'][20]['value'] / 1023 * tm_diff * 300000

>>>>>>> Add basic physics system
        # Simulate the drivetrain
        lf_motor = hal_data['CAN'][10]['value'] / 1023
        lr_motor = hal_data['CAN'][15]['value'] / 1023
        rf_motor = hal_data['CAN'][20]['value'] / 1023
        rr_motor = hal_data['CAN'][25]['value'] / 1023

        speed, rotation = self.drivetrain.get_vector(-lr_motor, -rr_motor, -lf_motor, -rf_motor)

        self.controller.drive(speed, rotation, tm_diff)

        self.left_encoder += self.drivetrain.l_speed * tm_diff
        self.right_encoder += self.drivetrain.r_speed * tm_diff

        hal_data['encoder'][0]['count'] = int(self.right_encoder * self.encoder_ticks)
        hal_data['encoder'][1]['count'] = int(self.left_encoder * self.encoder_ticks)
