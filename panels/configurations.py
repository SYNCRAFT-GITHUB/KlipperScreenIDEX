import logging
import random
import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

from ks_includes.KlippyGcodes import KlippyGcodes
from ks_includes.screen_panel import ScreenPanel


class Panel(ScreenPanel):

    def __init__(self, screen, title):

        super().__init__(screen, title)
        self.menu = ['configurations']

        class ConfigurationButton:
            def __init__(self, button: str, panel: str, title: str, icon: str, show: bool = True):
                self.button = button
                self.icon = icon
                self.panel = panel
                self.title = title
                self.show = show

        self.config_buttons = [
            ConfigurationButton(button='SYNCRAFT', panel="syncraft_panel", title=_("Syncraft"), icon='syncraft'),
            ConfigurationButton(button='CALIBRATE', panel='calibrate', title=_("Calibrate"), icon='calibrate'),
            ConfigurationButton(button='SETTINGS', panel='settings', title=_("Settings"), icon='settings'),
            ConfigurationButton(button='POWER', panel='power', title=_("Power"), icon='shutdown'),
            # ConfigurationButton(button='DEV02', panel='input_shaper', title="input_shaper", icon='custom-script'),
            # ConfigurationButton(button='DEV03', panel='gcode_macros', title="gcode_macros", icon='custom-script'),
            # ConfigurationButton(button='DEV04', panel='led', title="led", icon='custom-script'),
            # ConfigurationButton(button='DEV05', panel='limits', title="limits", icon='custom-script'),
            # ConfigurationButton(button='DEV06', panel='notifications', title="notifications", icon='custom-script'),
            # ConfigurationButton(button='DEV07', panel='retraction', title="retraction", icon='custom-script'),
            # ConfigurationButton(button='DEV08', panel='spoolman', title="spoolman", icon='custom-script'),
        ]

        grid = self._gtk.HomogeneousGrid()
        scroll = self._gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(grid)
        self.content.add(scroll)

        columns = 2

        for i, btn in enumerate(self.config_buttons):

            self.button = self._gtk.Button(btn.icon, btn.title, f"color{random.randint(1, 4)}")
            
            self.button.connect("clicked", self.menu_item_clicked, {
                "name": _(btn.title),
                "panel": btn.panel
            })

            if self._screen.vertical_mode:
                row = i % columns
                col = int(i / columns)
            else:
                col = i % columns
                row = int(i / columns)
            grid.attach(self.button, col, row, 1, 1)

        self.labels['configurations'] = self._gtk.HomogeneousGrid()
        self.labels['configurations'].attach(grid, 0, 0, 1, 2)

        self.content.add(self.labels['configurations'])