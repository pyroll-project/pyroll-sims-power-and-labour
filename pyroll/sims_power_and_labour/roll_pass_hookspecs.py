from pyroll.core import RollPass


@RollPass.hookspec
def equivalent_height_change(roll_pass: RollPass):
    """Height change of the equivalent flat roll pass"""


@RollPass.hookspec
def equivalent_reduction(roll_pass: RollPass):
    """Reduction of stock of the equivalent flat roll pass"""


@RollPass.hookspec
def equivalent_neutral_line_angle(roll_pass: RollPass):
    """Roll angle of the neutral line for the equivalent flat roll pass"""


@RollPass.hookspec
def equivalent_height_at_neutral_line(roll_pass: RollPass):
    """Workpiece height at the neutral for the equivalent flat roll pass"""


@RollPass.hookspec
def sims_force_function(roll_pass: RollPass):
    """Function developed by R.B. Sims for calculation of the roll force"""


@RollPass.hookspec
def sims_torque_function(roll_pass: RollPass):
    """Function developed by R.B. Sims for calculation of the roll torque"""
