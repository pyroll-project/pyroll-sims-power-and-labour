from pyroll.core import RollPass
from pyroll.ui import Exporter
from pyroll.utils import for_units


@Exporter.hookimpl
@for_units(RollPass)
def columns(unit: RollPass):
    return dict(
        lever_arm_coefficient_sims=f"{unit.lever_arm_sims:.2f}",
        roll_torque_general=f"{unit.roll.roll_torque_general:.2f}"
    )
