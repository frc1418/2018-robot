import math

from networktables.util import ntproperty
import wpilib
import ctre
from pyfrc.physics.drivetrains import four_motor_drivetrain


class PhysicsEngine:

    def __init__(self, controller):
        self.controller = controller

        self.controller.add_device_gyro_channel('navxmxp_spi_4_angle')

    def initialize(self, hal_data):
        # TODO Add network tables position and rotation link
        self.r_rotate_encoder = 0
        self.l_rotate_encoder = 0

    def update_sim(self, hal_data, now, tm_diff):
        """
        Update pyfrc simulator.
        :param hal_data: Data about motors and other components
        :param now: Current time in ms
        :param tm_diff: Difference between current time and time when last checked
        """
        self.l_rotate_encoder += hal_data['pwm'][0]['value'] * tm_diff * 20
        self.r_rotate_encoder += hal_data['pwm'][1]['value'] * tm_diff * 20

        self.l_rotate_encoder %= 5
        self.r_rotate_encoder %= 5

        hal_data['analog_in'][0]['avg_voltage'] = self.l_rotate_encoder
        hal_data['analog_in'][1]['avg_voltage'] = self.r_rotate_encoder

        # Only use front motors to get encoder positions
        # RR Motor
        hal_data['CAN'][15]['quad_position'] += hal_data['CAN'][25]['value'] / 1023 * tm_diff * 300000
        # RL Motor
        hal_data['CAN'][10]['quad_position'] -= hal_data['CAN'][20]['value'] / 1023 * tm_diff * 300000
        # FR Motor
        hal_data['CAN'][15]['quad_position'] += hal_data['CAN'][15]['value'] / 1023 * tm_diff * 300000
        # FL Motor
        hal_data['CAN'][10]['quad_position'] -= hal_data['CAN'][10]['value'] / 1023 * tm_diff * 300000

        rr_motor = hal_data['CAN'][25]['value'] / 1023
        lr_motor = -hal_data['CAN'][20]['value'] / 1023
        rf_motor = hal_data['CAN'][15]['value'] / 1023
        lf_motor = -hal_data['CAN'][10]['value'] / 1023

        fwd, rcw = four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor, x_wheelbase=3, speed=9)
        self.controller.drive(fwd, rcw, tm_diff)
