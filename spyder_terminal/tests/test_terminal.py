# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
#

"""Tests for the plugin."""

# Test library imports
import os
import pytest
import os.path
from qtpy.QtCore import Qt
from qtpy.QtWebEngineWidgets import WEBENGINE

# Local imports
from spyder_terminal.terminalplugin import TerminalPlugin

LOCATION = os.path.realpath(os.path.join(os.getcwd(),
                                         os.path.dirname(__file__)))

TERM_UP = 5000


def check_pwd(termwidget):
    """Check if pwd command is executed."""
    if WEBENGINE:
        def callback(data):
            global html
            html = data
        termwidget.body.toHtml(callback)
        try:
            return LOCATION in html
        except NameError:
            return False
    else:
        return LOCATION in termwidget.body.toHtml()


@pytest.fixture
def setup_terminal(qtbot):
    """Set up the Notebook plugin."""
    terminal = TerminalPlugin(None)
    qtbot.addWidget(terminal)
    terminal.create_new_term()
    terminal.show()
    return terminal


def test_new_terminal(qtbot):
    """Test if a new terminal is added."""
    # Setup widget
    terminal = setup_terminal(qtbot)
    term = terminal.get_current_term()
    qtbot.wait(1000)

    # Move to LOCATION
    qtbot.keyClicks(term.view, 'cd {}'.format(LOCATION))
    qtbot.keyPress(term.view, Qt.Key_Return)

    # Run pwd
    qtbot.keyClicks(term.view, 'pwd')
    qtbot.keyPress(term.view, Qt.Key_Return)

    # Assert pwd is LOCATION
    qtbot.waitUntil(lambda: check_pwd(term), timeout=TERM_UP)
    assert len(terminal.terms) == 1

