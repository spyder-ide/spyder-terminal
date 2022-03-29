# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
#

"""Tests for the plugin."""

# Test library imports

import os
import os.path as osp
import pytest
import requests
import sys
from flaky import flaky
from pytestqt.plugin import QtBot
from unittest.mock import Mock
from qtpy.QtWidgets import QMainWindow, QApplication
from spyder.config.manager import CONF

os.environ['SPYDER_DEV'] = 'True'

# Local imports
import spyder_terminal.terminalplugin
from spyder_terminal.terminalplugin import TerminalPlugin

LOCATION = os.path.realpath(os.path.join(os.getcwd(),
                                         os.path.dirname(__file__)))
LOCATION_SLASH = LOCATION.replace('\\', '/')

TERM_UP = 10000
WINDOWS = os.name == 'nt'

EXIT = 'exit'
CLEAR = 'clear'
if WINDOWS:
    CLEAR = 'cls'

PWD = 'pwd'
if WINDOWS:
    PWD = 'cd'

PREFIX = 'spyder_terminal.default.'


def check_pwd(termwidget):
    """Check if pwd command is executed."""
    def callback(data):
        global html
        html = data
    termwidget.body.runJavaScript(PREFIX + "getTerminalLines()", callback)
    try:
        return LOCATION in html
    except NameError:
        return False


def check_paste(termwidget, expected):
    """Check if pasting is correct in the terminal."""
    def callback(data):
        global text
        text = data
    termwidget.body.runJavaScript(PREFIX + "getTerminalLines()", callback)
    try:
        return all([x in text for x in expected])
    except NameError:
        return False


def check_output(termwidget, expected):
    """Check if the output includes the expected string."""
    def callback(data):
        global text
        text = data
    termwidget.body.runJavaScript(PREFIX + "getTerminalLines()", callback)
    try:
        return expected in text
    except NameError:
        return False


def check_increase_font_size(term):
    def callback(data):
        global font_size
        font_size = data
    expected = 15
    term.body.runJavaScript(PREFIX + "increaseFontSize()", callback)
    try:
        return font_size > expected
    except NameError:
        return False


def check_decrease_font_size(term):
    def callback(data):
        global font_size
        font_size = data
    expected = 16
    term.body.runJavaScript(PREFIX + "decreaseFontSize()", callback)
    try:
        return font_size < expected
    except NameError:
        return False


def check_fonts(term, expected):
    """Check if terminal fonts were updated."""
    def callback(data):
        global term_fonts
        term_fonts = data
    term.body.runJavaScript(PREFIX + "getFonts()", callback)
    try:
        return term_fonts == expected
    except NameError:
        return False


def check_hex_to_rgb(term):
    """Check if terminal is converting hexa colors to rgb correctly."""
    def callback(data):
        global hex_to_rgb
        hex_to_rgb = data
    expected = 'rgba(170, 171, 33, 0.2)'
    color = '#aaab21'
    term.body.runJavaScript(PREFIX + "hexToRGB('{}')".format(color),
                            callback)
    try:
        return hex_to_rgb == expected
    except NameError:
        return False


def check_num_tabs(terminal, ref_value):
    """Check if total number of terminal tabs has changed."""
    value = len(terminal.get_widget().get_terms())
    return value != ref_value


@pytest.fixture(scope="module")
def qtbot_module(qapp, request):
    """Module fixture for qtbot."""
    result = QtBot(request)
    return result


@pytest.fixture(scope='module')
def setup_terminal(qtbot_module, request):
    """Set up the Notebook plugin."""
    class MainMock(QMainWindow):
        def __getattr__(self, attr):
            return Mock()

        def register_shortcut(self, *args, **kwargs):
            pass

    main = MainMock()
    CONF.register_plugin(TerminalPlugin)
    terminal = TerminalPlugin(main, CONF)
    terminal.update_font()
    qtbot_module.addWidget(terminal)
    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(5000)
    terminal.create_new_term()
    terminal.get_widget().show()

    def teardown():
        terminal.on_close()

    request.addfinalizer(teardown)
    return terminal


@flaky(max_runs=3)
@pytest.mark.skipif((os.environ.get('CI') and
                     sys.platform.startswith('linux')),
                    reason="Doesn't work on Linux CIs")
def test_terminal_paste(setup_terminal, qtbot_module):
    """Test the paste action in the terminal."""
    terminal = setup_terminal
    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)

    term = terminal.get_widget().get_current_term()
    port = terminal.get_widget().port
    status_code = requests.get('http://127.0.0.1:{}'.format(port)).status_code
    assert status_code == 200

    term.exec_cmd(f'{os.linesep}' * 2)

    separator = os.linesep
    expected = ['prueba']
    QApplication.clipboard().clear()
    QApplication.clipboard().setText(separator.join(expected))
    term.view.paste()
    qtbot_module.waitUntil(lambda: check_paste(term, expected),
                           timeout=TERM_UP)

    expected = ['this', 'a', 'test']
    QApplication.clipboard().setText(separator.join(expected))
    term.view.paste()
    qtbot_module.waitUntil(lambda: check_paste(term, expected),
                           timeout=TERM_UP)


def test_terminal_color(setup_terminal, qtbot_module):
    """Test if the terminal color is converting to rgba correctly."""
    terminal = setup_terminal
    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)

    term = terminal.get_widget().get_current_term()
    port = terminal.get_widget().port
    status_code = requests.get('http://127.0.0.1:{}'.format(port)).status_code
    assert status_code == 200
    qtbot_module.waitUntil(lambda: check_hex_to_rgb(term),  timeout=TERM_UP)


def test_terminal_find(setup_terminal, qtbot_module):
    """Test the terminal find next/previous functions."""
    terminal = setup_terminal
    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)

    term = terminal.get_widget().get_current_term()
    port = terminal.get_widget().port
    status_code = requests.get('http://127.0.0.1:{}'.format(port)).status_code
    assert status_code == 200

    term.exec_cmd('ls')
    qtbot_module.wait(1000)

    # Search without any special parameters
    text = 'ls'
    found = term.search_next(text)
    assert found != -1
    found = term.search_previous(text)
    assert found != -1

    # Search with case sensitive search
    text = 'ls'
    found = term.search_next(text, case=True)
    assert found != -1
    found = term.search_previous(text, case=True)
    assert found != -1

    # Search with the regex option
    text = r'/\((.*?)\)/'
    found = term.search_next(text, regex=True)
    assert found != -1
    found = term.search_previous(text, regex=True)
    assert found != -1

    # Search whole word option
    text = 'ls'
    found = term.search_next(text, word=True)
    assert found != -1
    found = term.search_previous(text, word=True)
    assert found != -1


def test_terminal_font(setup_terminal, qtbot_module):
    """Test if terminal loads a custom font."""
    terminal = setup_terminal

    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)

    term = terminal.get_widget().get_current_term()
    port = terminal.get_widget().port
    status_code = requests.get('http://127.0.0.1:{}'.format(port)).status_code
    assert status_code == 200
    term.set_font('Ubuntu Mono')
    expected = '\'Ubuntu Mono\', monospace'
    qtbot_module.waitUntil(lambda: check_fonts(term, expected),
                           timeout=TERM_UP)
    # Verify increase of size of font
    qtbot_module.waitUntil(lambda: check_increase_font_size(term),
                           timeout=TERM_UP)
    # Verify decrease of size of font
    qtbot_module.waitUntil(lambda: check_decrease_font_size(term),
                           timeout=TERM_UP)


def test_terminal_tab_title(setup_terminal, qtbot_module):
    """Test if terminal tab titles are numbered sequentially."""
    terminal = setup_terminal

    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)
    terminal.create_new_term()
    terminal.create_new_term()
    num_1 = int(terminal.get_widget().tabwidget.tabText(1)[-1])
    num_2 = int(terminal.get_widget().tabwidget.tabText(2)[-1])
    assert num_2 == num_1 + 1


@flaky(max_runs=3)
@pytest.mark.skipif((os.environ.get('CI') and
                     sys.platform.startswith('linux')),
                    reason="Doesn't work on Linux CIs")
def test_new_terminal(setup_terminal, qtbot_module):
    """Test if a new terminal is added."""
    # Setup widget
    terminal = setup_terminal
    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)

    # Test if server is running
    port = terminal.get_widget().port
    status_code = requests.get('http://127.0.0.1:{}'.format(port)).status_code
    assert status_code == 200

    terminal.create_new_term()
    term = terminal.get_widget().get_current_term()
    qtbot_module.wait(1000)
    # Move to LOCATION
    # qtbot_module.keyClicks(term.view, 'cd {}'.format(LOCATION))
    # qtbot_module.keyPress(term.view, Qt.Key_Return)
    term.exec_cmd('cd {}'.format(LOCATION_SLASH))

    # Clear
    # qtbot_module.keyClicks(term.view, 'clear')
    # qtbot_module.keyPress(term.view, Qt.Key_Return)
    term.exec_cmd(CLEAR)

    # Run pwd
    # qtbot_module.keyClicks(term.view, 'pwd')
    # qtbot_module.keyPress(term.view, Qt.Key_Return)
    qtbot_module.wait(3000)
    term.exec_cmd(PWD)
    qtbot_module.wait(1000)

    # Assert pwd is LOCATION
    term.resize(900, 700)
    qtbot_module.waitUntil(lambda: check_pwd(term), timeout=TERM_UP)


def test_output_redirection(setup_terminal, qtbot_module):
    """Test if stdout and stderr are redirected on DEV mode."""
    assert spyder_terminal.widgets.main_widget.get_debug_level() > 0

    stdout = osp.join(os.getcwd(), 'spyder_terminal_out.log')
    stderr = osp.join(os.getcwd(), 'spyder_terminal_err.log')
    assert osp.exists(stdout) and osp.exists(stderr)


@flaky(max_runs=3)
@pytest.mark.skipif(os.name == 'nt', reason="It hangs on Windows")
def test_close_terminal_manually(setup_terminal, qtbot_module):
    """Test if terminal tab is closed after process was finished manually."""
    # Setup widget
    terminal = setup_terminal
    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)

    terminal.create_new_term()
    initial_num = len(terminal.get_widget().get_terms())
    term = terminal.get_widget().get_current_term()
    qtbot_module.wait(3000)

    term.exec_cmd(EXIT)

    qtbot_module.waitUntil(lambda: check_num_tabs(terminal, initial_num),
                           timeout=TERM_UP)
    final_num = len(terminal.get_widget().get_terms())
    assert final_num == initial_num - 1


def test_terminal_cwd(setup_terminal, qtbot_module):
    """Test if the a new terminal supports cwd  with especial characters."""
    start_dir = os.getcwd()
    new_dir = osp.join(start_dir, 'this is dir with spaces')
    if not osp.exists(new_dir):
        os.mkdir(new_dir)
    os.chdir(new_dir)

    terminal = setup_terminal
    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)

    port = terminal.get_widget().port
    status_code = requests.get('http://127.0.0.1:{}'.format(port)).status_code
    assert status_code == 200

    # Revert cwd
    os.chdir(start_dir)


@flaky(max_runs=3)
@pytest.mark.skipif(sys.platform == 'darwin', reason="It hangs on macOS")
def test_conda_path(setup_terminal, qtbot_module):
    """Test if conda is correctly added to the path of the terminal."""
    terminal = setup_terminal
    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)

    term = terminal.get_widget().get_current_term()
    # Check that conda list works
    term.exec_cmd("conda env list")
    qtbot_module.waitUntil(lambda: check_output(term, "test"), timeout=TERM_UP)

    # Clear the terminal
    term.exec_cmd("clear")

    # Try to deactivate the current environment
    term.exec_cmd("conda deactivate")
    qtbot_module.waitUntil(lambda: check_output(term, "base"), timeout=TERM_UP)


def test_zoom(setup_terminal, qtbot_module):
    """Test zoom level is increasing and decreasing."""
    terminal = setup_terminal
    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)

    term = terminal.get_widget().get_current_term()
    original_zoom = term.get_conf("zoom")

    term.view.increase_font()
    term.view.increase_font()
    term.view.increase_font()

    # Check the zoom increases three times
    assert term.get_conf("zoom") == original_zoom + 3

    term.view.decrease_font()
    term.view.decrease_font()

    # Check the zoom decreases two times
    assert term.get_conf("zoom") == original_zoom + 1


def test_zoom_new_term(setup_terminal, qtbot_module):
    """Test zoom level is correct when creating a new terminal."""
    terminal = setup_terminal
    qtbot_module.waitUntil(
        lambda: terminal.get_widget().server_is_ready(), timeout=TERM_UP)
    qtbot_module.wait(1000)

    term = terminal.get_widget().get_current_term()

    term.view.increase_font()
    term.view.increase_font()
    term1_zoom = term.get_conf("zoom")

    terminal.create_new_term()
    term = terminal.get_widget().get_current_term()
    new_zoom = term.get_conf("zoom")

    assert term1_zoom == new_zoom