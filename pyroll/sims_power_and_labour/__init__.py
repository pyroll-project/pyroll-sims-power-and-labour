from pyroll.core import RollPass, Roll

from . import roll_pass_hookspecs, roll_hookspecs
from . import roll_pass_hookimpls, roll_hookimpls

RollPass.plugin_manager.add_hookspecs(roll_pass_hookspecs)
RollPass.plugin_manager.register(roll_pass_hookimpls)

RollPass.Roll.plugin_manager.register(roll_pass_hookimpls)

Roll.plugin_manager.register(roll_hookimpls)
Roll.plugin_manager.add_hookspecs(roll_hookspecs)
