from pyroll.core import RollPass


@RollPass.Roll.hookspec
def roll_torque_general(roll_pass: RollPass, roll: RollPass.Roll):
    """Roll torque calculated by a method from K. H. Weber."""
