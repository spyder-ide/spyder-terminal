# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)
"""Spyder terminal configuration page."""

# Third party imports
import os
from qtpy.QtWidgets import (QVBoxLayout, QGroupBox, QGridLayout, QButtonGroup,
                            QRadioButton, QWidget)

# Local imports
from spyder.api.preferences import PluginConfigPage
from spyder.config.base import _
from spyder.utils.programs import find_program

WINDOWS = os.name == 'nt'
UNIX_SHELLS = ['bash', 'sh', 'ksh', 'zsh', 'csh', 'pwsh']
WINDOWS_SHELLS = ['cmd', 'powershell']


class TerminalConfigPage(PluginConfigPage):
    def setup_page(self):
        """Create configuration page."""
        terminal_widget = QWidget
        options_layout = QGridLayout()
        # Custom shell options
        shell_widget = QGroupBox(_("Terminal shell"))
        shell_layout = QVBoxLayout()
        if WINDOWS:
            self.shells = WINDOWS_SHELLS
        else:
            self.shells = UNIX_SHELLS

        valid_shells = []
        for shell in self.shells:
            if find_program(shell) is not None:
                valid_shells.append(shell)
        shell_choices = list(zip(valid_shells, valid_shells))
        shell_combo = self.create_combobox(_("Select the shell interpreter:"),
                                           shell_choices, 'shell',
                                           restart=True)
        shell_combo.combobox.setMinimumContentsLength(15)
        shell_layout.addWidget(shell_combo)
        shell_widget.setLayout(shell_layout)
        shell_layout.addStretch(1)
        options_layout.addWidget(shell_widget)

        # Style preferences
        terminal_widget = QGroupBox(_("Terminal style preferences"))
        # Custom bar option
        cursor_options = [_("block"), _("underline"), _("bar")]
        cursor_choices = list(zip(cursor_options,
                                  [c.lower() for c in cursor_options]))
        self.cursor_combo = self.create_combobox(_("Type of cursor:"),
                                                 cursor_choices,
                                                 'cursor_type',
                                                 default='bar')
        self.cursor_combo.combobox.setMinimumContentsLength(15)
        options_layout.addWidget(self.cursor_combo)

        # Custom sound option
        self.sound_cb = self.create_checkbox(
            _("Enable bell sound"), 'sound',
            tip=_("Enable bell sound on terminal"))
        options_layout.addWidget(self.sound_cb)

        terminal_widget.setLayout(options_layout)

        layout = QVBoxLayout()
        layout.addWidget(shell_widget)
        layout.addWidget(terminal_widget)
        layout.addStretch(1)

        self.setLayout(layout)
