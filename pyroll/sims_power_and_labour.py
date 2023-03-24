import logging
import numpy as np
import scipy.optimize as opt
from pyroll.core import RollPass, Hook

VERSION = "2.0"

log = logging.getLogger(__name__)

RollPass.inverse_forming_efficiency = Hook[float]()
"""Inverse forming efficiency of the roll pass."""

RollPass.roll_torque_loss_function = Hook[float]()
"""Loss function defined by R.B Sims for the roll torque for the roll pass."""

RollPass.equivalent_entry_angle = Hook[float]()
"""Entry angle of the equivalent flat pass into the roll pass."""

RollPass.Roll.neutral_angle = Hook[float]()
"""Angle of the neutral point at the roll surface according to R.B. Sims."""

RollPass.Roll.lever_arm = Hook[float]()
"""Lever arm of the roll according to R.B. Sims."""


@RollPass.equivalent_entry_angle
def equivalent_entry_angle(self: RollPass):
    entry_angle = np.arcsin(self.roll.contact_length / self.roll.min_radius)
    log.info(f"Calculated an entry angle of: {np.rad2deg(entry_angle):.2f}")
    return entry_angle


@RollPass.Roll.neutral_angle
def neutral_angle(self: RollPass.Roll):
    rp = self.roll_pass
    def sims_full_neutral_line_angle_function(neutral_line_angle: float):
        return (2 * np.sqrt(self.flattened_radius / rp.out_profile.equivalent_height) * np.arctan(
            np.sqrt(self.flattened_radius / rp.out_profile.equivalent_height)) * neutral_line_angle - np.sqrt(
            self.flattened_radius / rp.out_profile.equivalent_height) * np.arctan(
            np.sqrt(
                self.flattened_radius / rp.out_profile.equivalent_height)) * rp.equivalent_entry_angle) - np.pi / 4 * np.log(
            rp.in_profile.equivalent_height / rp.out_profile.equivalent_height)

    def sims_simplified_neutral_line_angle():
        return np.sqrt(rp.out_profile.equivalent_height / self.flattened_radius) * np.tan(1 / 2 * (
                np.arctan(
                    np.sqrt(rp.in_profile.equivalent_height / rp.out_profile.equivalent_height - 1)) + np.sqrt(
            rp.out_profile.equivalent_height / self.flattened_radius) * np.pi / 4 * np.log(
            rp.out_profile.equivalent_height / rp.in_profile.equivalent_height)
        ))


    neutral_line_angle_from_full_function = opt.root(sims_full_neutral_line_angle_function,
                                                     self.contact_length / 2)

    if neutral_line_angle_from_full_function.success is True:
        neutral_line_angle = neutral_line_angle_from_full_function.x[0]
        log.info(f"Calculated a neutral line angle of {np.rad2deg(neutral_line_angle):.2f} using Sims original model")
    else:
        neutral_line_angle = sims_simplified_neutral_line_angle()
        log.warning(
            "Calculation of neutral line angle using Sims original model failed due to" + neutral_line_angle_from_full_function.message)
        log.info(f"Calculated a neutral line angle of {np.rad2deg(neutral_line_angle):.2f} using Sims simplified model")

    return neutral_line_angle


@RollPass.inverse_forming_efficiency
def inverse_forming_efficiency(self: RollPass):
    height_at_neutral_angle = self.out_profile.equivalent_height + self.roll.flattened_radius * self.roll.neutral_angle ** 2
    eq_drought = self.in_profile.equivalent_height - self.out_profile.equivalent_height

    a = np.sqrt((1 - eq_drought) / eq_drought)
    b = np.sqrt(eq_drought / (1 - eq_drought))
    c = np.sqrt(self.roll.flattened_radius / self.out_profile.equivalent_rectangle.height)

    return np.pi / 2 * a * np.arctan(b) - np.pi / 4 - a * c * np.log(
        height_at_neutral_angle / self.out_profile.equivalent_height) + 1 / 2 * a * c * np.log(
        1 / (1 - eq_drought))


@RollPass.roll_force
def roll_force(self: RollPass):
    eq_drought = self.in_profile.equivalent_height - self.out_profile.equivalent_height
    mean_flow_stress = (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3
    mean_width = (self.in_profile.equivalent_width + 2 * self.out_profile.equivalent_width) / 3

    roll_force_per_width = mean_flow_stress * np.sqrt(
        self.roll.flattened_radius * eq_drought) * self.inverse_forming_efficiency

    return - roll_force_per_width * mean_width


@RollPass.Roll.lever_arm
def lever_arm(self: RollPass.Roll):
    rp = self.roll_pass
    return 0.78 + 0.017 * self.flattened_radius / rp.out_profile.equivalent_height - 0.163 * np.sqrt(
        self.flattened_radius / rp.out_profile.equivalent_height)


@RollPass.roll_torque_loss_function
def roll_torque_loss_function(self: RollPass):
    return self.equivalent_entry_angle / 2 - self.roll.neutral_angle


@RollPass.Roll.roll_torque
def roll_torque(self: RollPass.Roll):
    rp = self.roll_pass
    mean_flow_stress = (rp.in_profile.flow_stress + 2 * rp.out_profile.flow_stress) / 3
    mean_width = (rp.in_profile.equivalent_width + 2 * rp.out_profile.equivalent_width) / 3

    torque_per_width = self.working_radius * self.flattened_radius * mean_flow_stress * rp.roll_torque_loss_function

    return - torque_per_width * mean_width
