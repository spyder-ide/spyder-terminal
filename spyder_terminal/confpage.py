# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""Spyder terminal configuration page."""

# Standard library imports
import os
import sys

# Third party imports
from qtpy.QtWidgets import QVBoxLayout, QGroupBox, QGridLayout
from spyder.api.preferences import PluginConfigPage
from spyder.config.base import get_translation
from spyder.utils.programs import find_program

# Constants
WINDOWS = os.name == 'nt'
UNIX_SHELLS = ['bash', 'sh', 'ksh', 'zsh', 'csh', 'pwsh', 'rbash', 'dash',
               'screen', 'tmux', 'tcsh', 'fish', 'xonsh']
WINDOWS_SHELLS = ['cmd', 'powershell', 'xonsh']

# For translations
_ = get_translation('spyder_terminal')


class TerminalConfigPage(PluginConfigPage):
    def setup_page(self):
        """Create configuration page."""
        options_layout = QGridLayout()
        # Custom shell options
        shell_group = QGroupBox(_("Terminal shell"))
        shell_layout = QVBoxLayout()
        if WINDOWS:
            self.shells = WINDOWS_SHELLS
        else:
            self.shells = UNIX_SHELLS

        valid_shells = []
        for shell in self.shells:
            if find_program(shell) is not None:
                valid_shells.append(shell)
        valid_shells = zip(valid_shells, valid_shells)
        if WINDOWS:
            default_option = 'cmd'
        elif sys.platform.startswith('linux'):
            default_option = 'bash'
        elif 'bsd' in sys.platform:
            default_option = 'sh'
        else:
            default_option = 'zsh'
        shell_combo = self.create_combobox(_("Select the shell interpreter:"),
                                           valid_shells, 'shell', restart=True,
                                           default=default_option)
        shell_combo.combobox.setMinimumContentsLength(15)
        shell_layout.addWidget(shell_combo)
        shell_group.setLayout(shell_layout)
        shell_layout.addStretch(1)
        options_layout.addWidget(shell_group)

        # Display preferences
        display_group = QGroupBox(_("Terminal display preferences"))
        display_layout = QVBoxLayout()
        # Custom buffer limit
        self.buffer_sb = self.create_spinbox(_("Buffer limit: "), "",
                                             'buffer_limit', min_=100,
                                             default=1000,
                                             max_=1000000, step=1)
        display_layout.addWidget(self.buffer_sb)
        display_group.setLayout(display_layout)
        display_layout.addStretch(1)
        options_layout.addWidget(display_group)

        # Style preferences
        terminal_group = QGroupBox(_("Terminal style preferences"))
        # Custom bar option
        cursor_choices = [(_("Block"), 0), (_("Underline"), 1), (_("Bar"), 2)]
        self.cursor_combo = self.create_combobox(_("Type of cursor:"),
                                                 cursor_choices,
                                                 'cursor_type')
        self.cursor_combo.combobox.setMinimumContentsLength(15)
        options_layout.addWidget(self.cursor_combo)

        # Custom sound option
        self.sound_cb = self.create_checkbox(
            _("Enable bell sound"), 'sound',
            tip=_("Enable bell sound on terminal"))
        options_layout.addWidget(self.sound_cb)

        # Visual bell option
        self.cursor_blink_cb = self.create_checkbox(
            _("Enable cursor blink"), 'cursor_blink',
            tip=_("_Enable cursor blink on terminal"))
        options_layout.addWidget(self.cursor_blink_cb)

        terminal_group.setLayout(options_layout)

        layout = QVBoxLayout()
        layout.addWidget(shell_group)
        layout.addWidget(display_group)
        layout.addWidget(terminal_group)
        layout.addStretch(1)

        self.setLayout(layout)
