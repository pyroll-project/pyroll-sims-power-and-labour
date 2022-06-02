from pyroll.core import RollPass
from pyroll.ui import Reporter
from pyroll.utils import for_units


@Reporter.hookimpl
@for_units(RollPass)
def unit_properties(unit: RollPass):
    return dict(
        lever_arm_coefficient_sims=f"{unit.lever_arm_sims:.2f}",
        roll_torque_general=f"{unit.roll.roll_torque_general:.2f}"
    )
