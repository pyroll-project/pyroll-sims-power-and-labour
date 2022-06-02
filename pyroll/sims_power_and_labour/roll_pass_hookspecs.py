from pyroll.core import RollPass


@RollPass.hookspec
def equivalent_height_change(roll_pass: RollPass):
    """Equivalent height change."""


@RollPass.hookspec
def equivalent_reduction(roll_pass: RollPass):
    """Equivalent reduction of stock."""


@RollPass.hookspec
def equivalent_entry_angle(roll_pass: RollPass):
    """Equivalent roll angle at the first contact point."""


@RollPass.hookspec
def sims_neutral_line_angle(roll_pass: RollPass):
    """Neutral line angle from R.B. Sims for hot rolling."""


@RollPass.hookspec
def sims_simplified_neutral_line_angle(roll_pass: RollPass):
    """Simplified neutral line angle from R.B. Sims for hot rolling."""


@RollPass.hookspec
def equivalent_neutral_line_angle(roll_pass: RollPass):
    """Equivalent roll angle of the neutral line."""


@RollPass.hookspec
def equivalent_height_at_neutral_line(roll_pass: RollPass):
    """Equivalent workpiece height at the neutral line angle."""


@RollPass.hookspec
def lever_arm_sims(roll_pass: RollPass):
    """Lever arm coefficient approximated with a formula given by K. H. Weber."""


@RollPass.hookspec
def sims_force_function(roll_pass: RollPass):
    """Function developed by R.B. Sims for calculation of the roll force."""


@RollPass.hookspec
def sims_torque_function(roll_pass: RollPass):
    """Function developed by R.B. Sims for calculation of the roll torque."""
