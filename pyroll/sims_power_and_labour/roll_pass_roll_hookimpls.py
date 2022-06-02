from pyroll.core import RollPass


@RollPass.Roll.hookimpl
def roll_torque_general(roll_pass: RollPass, roll: RollPass.Roll):
    return roll_pass.roll_force * roll.contact_length * roll_pass.lever_arm_sims
