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
import requests
# from OpenGL import GL
from qtpy.QtCore import Qt
from qtpy.QtWebEngineWidgets import WEBENGINE

# Local imports
from spyder_terminal.terminalplugin import TerminalPlugin

LOCATION = os.path.realpath(os.path.join(os.getcwd(),
                                         os.path.dirname(__file__)))

TERM_UP = 10000


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


@pytest.fixture(scope="module")
def setup_terminal(qtbot):
    """Set up the Notebook plugin."""
    terminal = TerminalPlugin(None)
    qtbot.addWidget(terminal)
    terminal.create_new_term()
    terminal.show()
    return terminal


def test_terminal_font(qtbot):
    """Test if terminal loads a custom font."""
    terminal = setup_terminal(qtbot)
    term = terminal.get_current_term()
    qtbot.wait(TERM_UP)
    status_code = requests.get('http://127.0.0.1:8070').status_code
    assert status_code == 200
    term.set_font('Ubuntu Mono')
    fonts = term.get_fonts()
    assert fonts == "'Ubuntu Mono', ubuntu-powerline, monospace"
    terminal.closing_plugin()


def test_new_terminal(qtbot):
    """Test if a new terminal is added."""
    # Setup widget
    terminal = setup_terminal(qtbot)
    term = terminal.get_current_term()
    qtbot.wait(TERM_UP)

    # Test if server is running
    status_code = requests.get('http://127.0.0.1:8070').status_code
    assert status_code == 200

    # Move to LOCATION
    qtbot.keyClicks(term.view, 'cd {}'.format(LOCATION))
    qtbot.keyPress(term.view, Qt.Key_Return)

    # Clear
    qtbot.keyClicks(term.view, 'clear')
    qtbot.keyPress(term.view, Qt.Key_Return)

    # Run pwd
    qtbot.keyClicks(term.view, 'pwd')
    qtbot.keyPress(term.view, Qt.Key_Return)

    # Assert pwd is LOCATION
    qtbot.waitUntil(lambda: check_pwd(term), timeout=TERM_UP)
    assert len(terminal.terms) == 1
    terminal.closing_plugin()
