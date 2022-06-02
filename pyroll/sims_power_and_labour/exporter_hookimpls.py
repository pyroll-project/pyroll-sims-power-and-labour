from pyroll.core import RollPass
from pyroll.ui import Exporter
from pyroll.utils import for_units


@Exporter.hookimpl
@for_units(RollPass)
def columns(unit: RollPass):
    return dict(
        lever_arm_coefficient_weber=f"{unit.lever_arm_weber:.2f}",
        roll_torque_weber=f"{unit.roll.roll_torque_weber:.2f}"
    )
