from pyroll import RollPass


@RollPass.hookspec
def equivalent_height_change(roll_pass: RollPass):
    """"""


@RollPass.hookspec
def equivalent_reduction(roll_pass: RollPass):
    """"""


@RollPass.hookspec
def equivalent_neutral_line_angle(roll_pass: RollPass):
    """"""


@RollPass.hookspec
def equivalent_height_at_neutral_line(roll_pass: RollPass):
    """"""


@RollPass.hookspec
def sims_force_function(roll_pass: RollPass):
    """"""


@RollPass.hookspec
def sims_torque_function(roll_pass: RollPass):
    """"""
