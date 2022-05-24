import numpy as np
from pyroll.core import RollPass


@RollPass.hookimpl
def equivalent_height_change(roll_pass: RollPass):
    return roll_pass.in_profile.equivalent_rectangle.height - roll_pass.out_profile.equivalent_rectangle.height


@RollPass.hookimpl
def equivalent_reduction(roll_pass: RollPass):
    return 1 - roll_pass.out_profile.equivalent_rectangle.height / roll_pass.in_profile.equivalent_rectangle.height


@RollPass.hookimpl
def equivalent_neutral_line_angle(roll_pass: RollPass):
    return np.tan(1 / 8 * (
            4 * np.arctan(roll_pass.equivalent_reduction / (1 - roll_pass.equivalent_reduction)) + (np.pi * np.log(1 - roll_pass.equivalent_reduction)) / (
        np.sqrt(roll_pass.roll.flattened_radius / roll_pass.out_profile.equivalent_rectangle.height)))) / np.sqrt(
        roll_pass.roll.flattened_radius / roll_pass.out_profile.equivalent_rectangle.height)


@RollPass.hookimpl
def equivalent_height_at_neutral_line(roll_pass: RollPass):
    return roll_pass.out_profile.equivalent_rectangle.height + 2 * roll_pass.roll.flattened_radius * (1 - np.cos(roll_pass.equivalent_neutral_line_angle))


@RollPass.hookimpl
def sims_force_function(roll_pass: RollPass):
    reccuring_part_a = (1 - roll_pass.equivalent_reduction) / roll_pass.equivalent_reduction
    reccuring_part_b = roll_pass.equivalent_reduction / (1 - roll_pass.equivalent_reduction)
    reccuring_part_c = roll_pass.roll.flattened_radius / roll_pass.out_profile.equivalent_rectangle.height

    return np.pi / 2 * np.sqrt(reccuring_part_a) * np.arctan(np.sqrt(reccuring_part_b)) - np.pi / 4 - np.sqrt(reccuring_part_a) * np.sqrt(
        reccuring_part_c) * np.log(roll_pass.equivalent_height_at_neutral_line / roll_pass.out_profile.equivalent_rectangle.height) + 1 / 2 * np.sqrt(
        reccuring_part_a) * np.sqrt(reccuring_part_c) * np.log(1 / (1 - roll_pass.equivalent_reduction))


@RollPass.hookimpl
def roll_force(roll_pass: RollPass):
    mean_flow_stress = (roll_pass.in_profile.flow_stress + 2 * roll_pass.out_profile.flow_stress) / 3
    mean_width = (roll_pass.in_profile.equivalent_rectangle.width + roll_pass.out_profile.equivalent_rectangle.width) / 2

    return mean_flow_stress * np.sqrt(roll_pass.roll.flattened_radius * roll_pass.equivalent_height_change) * roll_pass.sims_force_function * mean_width


@RollPass.hookimpl
def sims_torque_function(roll_pass: RollPass):
    entry_angle = np.arcsin(roll_pass.roll.contact_length / roll_pass.roll.flattened_radius)
    return entry_angle / 2 - roll_pass.equivalent_neutral_line_angle


@RollPass.Roll.hookimpl
def roll_torque(roll_pass: RollPass, roll: RollPass.Roll):
    mean_flow_stress = (roll_pass.in_profile.flow_stress + 2 * roll_pass.out_profile.flow_stress) / 3
    return 2 * roll.nominal_radius * roll_pass.roll.flattened_radius * mean_flow_stress * roll_pass.sims_torque_function
