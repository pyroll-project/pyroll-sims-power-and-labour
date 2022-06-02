from pyroll.core import RollPass
from pyroll.ui import Reporter
from pyroll.utils import for_units


@Reporter.hookimpl
@for_units(RollPass)
def unit_properties(unit: RollPass):
    return dict(
        lever_arm_coefficient_weber=f"{unit.lever_arm_weber:.2f}",
        roll_torque_weber=f"{unit.roll.roll_torque_weber:.2f}"
    )
