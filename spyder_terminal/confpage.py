# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)
"""Spyder terminal configuration page."""

# Third party imports
from qtpy.QtWidgets import QTabWidget, QVBoxLayout, QWidget, QComboBox

# Local imports
from spyder.api.preferences import PluginConfigPage
from spyder.config.base import _
from spyder.py3compat import to_text_string
from spyder.plugins.explorer.widgets.fileassociations import (
    FileAssociationsWidget)


class TerminalConifgPage(PluginConfigPage):
    def setup_page(self):
        terminal_widget = QWidget()
        layout = QVBoxLayout()

        # Custom bar option
        cursor_combo_box = QComboBox(self)
        cursor_options = ['block', 'underline', 'bar']
        cursor_combo_box.addItems(cursor_options)
        layout.addWidget(cursor_combo_box)

        # Custom sound option
        sound_combo_box = QComboBox(self)
        sound_options = ['none', 'sound']
        sound_combo_box.addItems(sound_options)
        layout.addWidget(sound_combo_box)

        terminal_widget.setLayout(layout)
