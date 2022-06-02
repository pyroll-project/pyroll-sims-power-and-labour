from pyroll.core import RollPass


@RollPass.Roll.hookimpl
def roll_torque_weber(roll_pass: RollPass, roll: RollPass.Roll):
    return 2 * roll_pass.roll_force * roll.contact_length * roll_pass.lever_arm_weber
