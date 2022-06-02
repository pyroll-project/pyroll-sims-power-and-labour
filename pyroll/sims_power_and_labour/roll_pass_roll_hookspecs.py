from pyroll.core import RollPass


@RollPass.Roll.hookspec
def roll_torque_weber(roll_pass: RollPass, roll: RollPass.Roll):
    """Roll torque calculated by a method from K. H. Weber."""
