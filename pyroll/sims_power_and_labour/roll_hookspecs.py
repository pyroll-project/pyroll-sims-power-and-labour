from pyroll.core import Roll


@Roll.hookspec
def flattened_roll_radius(roll: Roll):
    """Flattened radius of the roll due to acting roll force."""
