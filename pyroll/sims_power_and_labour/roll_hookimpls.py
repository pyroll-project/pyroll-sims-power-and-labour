import logging

from pyroll.core import Roll

log = logging.getLogger(__name__)


@Roll.hookimpl
def flattened_roll_radius(roll: Roll):
    if not hasattr(roll, "flattened_radius"):
        log.warning("Due to missing model for flattened roll radius, working radius is used!")
        return roll.working_radius

    return roll.flattened_radius
