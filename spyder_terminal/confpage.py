# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)
"""Spyder terminal configuration page."""

# Third party imports
from qtpy.QtWidgets import (QVBoxLayout, QGroupBox, QGridLayout, QSpacerItem)

# Local imports
from spyder.api.preferences import PluginConfigPage
from spyder.config.base import _
from spyder_terminal.terminalplugin import TerminalPlugin


class TerminalConfigPage(PluginConfigPage):
    def setup_page(self):
        """Create configuration page."""
        terminal_widget = QGroupBox(_("Spyder Terminal"))
        options_layout = QGridLayout()

        # Custom bar option
        cursor_options = [_("block"), _("underline"), _("bar")]
        cursor_choices = list(zip(cursor_options,
                                  [c.lower() for c in cursor_options]))
        self.cursor_combo = self.create_combobox(_("Type of cursor:"),
                                                 cursor_choices,
                                                 'cursor_type',
                                                 default='bar')
        options_layout.addWidget(self.cursor_combo.label, 0, 0)
        options_layout.addWidget(self.cursor_combo.combobox, 0, 1)

        # Custom sound option
        self.sound_cb = self.create_checkbox(
            _("Enable bell sound"), 'sound',
            tip=_("Enable bell sound on terminal"))
        options_layout.addWidget(self.sound_cb)

        terminal_widget.setLayout(options_layout)

        layout = QVBoxLayout()
        layout.addWidget(terminal_widget)
        layout.addStretch(1)

        self.setLayout(layout)

    def apply_plugin_settings(self):
        """Apply the config settings."""
        cursor_style = self.cursor_combo.currentText()
        term_options = {'sound': self.sound_cb.isChecked(),
                        'cursor_style': cursor_style
                        }
        for plugin in self.main.thirdparty_plugins:
            if isinstance(plugin, TerminalPlugin):
                for term in plugin.get_terms():
                    term.apply_settings(term_options)
                for option in term_options:
                    self.set_option(option, term_options[option])
