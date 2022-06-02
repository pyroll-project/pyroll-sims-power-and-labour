from pyroll.core import RollPass, Roll
from pyroll.ui import Exporter, Reporter

from . import roll_pass_hookspecs, roll_hookspecs
from . import roll_pass_hookimpls, roll_hookimpls
from . import exporter_hookimpls, reporter_hookimpls
from . import roll_pass_roll_hookimpls, roll_pass_roll_hookspecs

RollPass.plugin_manager.add_hookspecs(roll_pass_hookspecs)
RollPass.plugin_manager.register(roll_pass_hookimpls)

RollPass.Roll.plugin_manager.register(roll_pass_hookimpls)

Roll.plugin_manager.register(roll_hookimpls)
Roll.plugin_manager.add_hookspecs(roll_hookspecs)

Exporter.plugin_manager.register(exporter_hookimpls)
Reporter.plugin_manager.register(reporter_hookimpls)

RollPass.Roll.plugin_manager.register(roll_pass_roll_hookimpls)
RollPass.Roll.plugin_manager.add_hookspecs(roll_pass_roll_hookspecs)
