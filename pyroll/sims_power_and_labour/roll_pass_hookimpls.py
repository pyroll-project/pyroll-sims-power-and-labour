import logging
import numpy as np
from pyroll.core import RollPass

log = logging.getLogger(__name__)


@RollPass.hookimpl
def equivalent_height_change(roll_pass: RollPass):
    return roll_pass.in_profile.equivalent_rectangle.height - roll_pass.out_profile.equivalent_rectangle.height


@RollPass.hookimpl
def equivalent_reduction(roll_pass: RollPass):
    return 1 - roll_pass.out_profile.equivalent_rectangle.height / roll_pass.in_profile.equivalent_rectangle.height


@RollPass.hookimpl
def equivalent_neutral_line_angle(roll_pass: RollPass):
    initial_height = roll_pass.in_profile.equivalent_rectangle.height
    final_height = roll_pass.out_profile.equivalent_rectangle.height

    sims_neutral_line = np.sqrt(final_height / roll_pass.roll.flattened_radius) * np.tan(1 / 2 * (
            np.arctan(np.sqrt(initial_height / final_height - 1)) + np.sqrt(final_height / roll_pass.roll.flattened_radius) * np.pi / 4 * np.log(
        final_height / initial_height)
    ))

    log.info(f"Calculated a neutral line angle of {np.rad2deg(sims_neutral_line):.2f} using Sims model")

    return sims_neutral_line


@RollPass.hookimpl
def equivalent_height_at_neutral_line(roll_pass: RollPass):
    return roll_pass.out_profile.equivalent_rectangle.height + roll_pass.roll.flattened_roll_radius * roll_pass.equivalent_neutral_line_angle ** 2


@RollPass.hookimpl
def sims_force_function(roll_pass: RollPass):
    a = np.sqrt((1 - roll_pass.equivalent_reduction) / roll_pass.equivalent_reduction)
    b = np.sqrt(roll_pass.equivalent_reduction / (1 - roll_pass.equivalent_reduction))
    c = np.sqrt(roll_pass.roll.flattened_roll_radius / roll_pass.out_profile.equivalent_rectangle.height)

    return np.pi / 2 * a * np.arctan(b) - np.pi / 4 - a * c * np.log(
        roll_pass.equivalent_height_at_neutral_line / roll_pass.out_profile.equivalent_rectangle.height) + 1 / 2 * a * c * np.log(
        1 / (1 - roll_pass.equivalent_reduction))


@RollPass.hookimpl
def roll_force(roll_pass: RollPass):
    mean_flow_stress = (roll_pass.in_profile.flow_stress + 2 * roll_pass.out_profile.flow_stress) / 3
    mean_width = (roll_pass.in_profile.equivalent_rectangle.width + roll_pass.out_profile.equivalent_rectangle.width) / 2
    roll_force_per_width = mean_flow_stress * np.sqrt(roll_pass.roll.flattened_roll_radius * roll_pass.equivalent_height_change) * roll_pass.sims_force_function

    return roll_force_per_width * mean_width


@RollPass.hookimpl
def sims_torque_function(roll_pass: RollPass):
    entry_angle = np.arcsin(roll_pass.roll.contact_length / roll_pass.roll.min_radius)
    log.info(f"Calculated an entry angle of: {np.rad2deg(entry_angle):.2f}")

    return entry_angle / 2 - roll_pass.equivalent_neutral_line_angle


@RollPass.Roll.hookimpl
def roll_torque(roll_pass: RollPass, roll: RollPass.Roll):
    mean_flow_stress = (roll_pass.in_profile.flow_stress + 2 * roll_pass.out_profile.flow_stress) / 3
    log.info(f"Calculated a mean flow stress of: {mean_flow_stress / 1e6 :.2f} MPa")
    mean_width = (roll_pass.in_profile.equivalent_rectangle.width + roll_pass.out_profile.equivalent_rectangle.width) / 2
    torque_per_width = 2 * roll.working_radius * roll.flattened_roll_radius * mean_flow_stress * roll_pass.sims_torque_function

    return torque_per_width * mean_width
