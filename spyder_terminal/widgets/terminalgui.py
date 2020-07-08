# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Terminal Widget."""
# Standard library imports
import json
import os
import sys

# Third-party imports
from qtpy.QtCore import (Qt, QUrl, Slot, QEvent, QTimer, Signal,
                         QObject)
from qtpy.QtGui import QKeySequence
from qtpy.QtWebChannel import QWebChannel
from qtpy.QtWebEngineWidgets import (QWebEnginePage, QWebEngineSettings,
                                     QWebEngineView)
from qtpy.QtWidgets import QMenu, QFrame, QVBoxLayout, QWidget, QApplication
from spyder.config.base import DEV, get_translation
from spyder.config.manager import CONF
from spyder.config.gui import is_dark_interface
from spyder.utils import icon_manager as ima
from spyder.utils.qthelpers import create_action, add_actions

# Local imports
from spyder_terminal.widgets.style.themes import ANSI_COLORS
from spyder_terminal.config import CONF_SECTION


PREFIX = 'spyder_terminal.default.'

# For translations
_ = get_translation('spyder_terminal')


class ChannelHandler(QObject):
    """QWebChannel handler for JS calls."""

    sig_ready = Signal()
    sig_closed = Signal()

    def __init__(self, parent):
        """Handler main constructor."""
        QObject.__init__(self, parent)

    @Slot()
    def ready(self):
        """Invoke signal when terminal prompt is ready."""
        self.sig_ready.emit()

    @Slot()
    def close(self):
        """Invoke signal when terminal process was closed externally."""
        self.sig_closed.emit()


class TerminalWidget(QFrame):
    """Terminal widget."""

    terminal_closed = Signal()
    terminal_ready = Signal()

    def __init__(self, parent, port, path='~', font=None, theme=None,
                 color_scheme=None):
        """Frame main constructor."""
        QWidget.__init__(self, parent)
        url = 'http://127.0.0.1:{0}?path={1}'.format(port, path)
        self.handler = ChannelHandler(self)
        self.handler.sig_ready.connect(lambda: self.terminal_ready.emit())
        self.handler.sig_closed.connect(lambda: self.terminal_closed.emit())
        self.view = TermView(self, parent.CONF,
                             term_url=url, handler=self.handler)
        self.font = font
        self.initial_path = path
        self.theme = theme
        self.color_scheme = color_scheme
        self.parent = parent
        self.shortcuts = self.create_shortcuts()
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLayout(layout)

        self.body = self.view.document

        self.handler.sig_ready.connect(self.setup_term)

    def setup_term(self):
        """Setup other terminal options after page has loaded."""
        # This forces to display the black background
        print("\0", end='')
        self.set_font(self.font)
        self.set_dir(self.initial_path)
        self.current_theme = self.set_theme(self.theme, self.color_scheme)
        self.set_scrollbar_style()
        options = self.parent.CONF.options(CONF_SECTION)
        dict_options = {}
        for option in options:
            dict_options[option] = self.parent.get_option(option)
        self.apply_settings(dict_options)

    def create_shortcuts(self):
        """Create the terminal shortcuts."""
        return self.view.create_shortcuts()

    def get_shortcut_data(self):
        """
        Return shortcut data, a list of tuples (shortcut, text, default).

        shortcut (QShortcut or QAction instance)
        text (string): action/shortcut description
        default (string): default key sequence
        """
        return self.view.get_shortcut_data()

    def eval_javascript(self, script):
        """Evaluate Javascript instructions inside view."""
        return self.view.eval_javascript(script)

    def set_scrollbar_style(self):
        """Set terminal scrollbar style."""
        if is_dark_interface():
            self.eval_javascript('addClassStyleToContainer("dark-scroll")')

    def set_dir(self, path):
        """Set terminal initial current working directory."""
        self.eval_javascript('setcwd("{0}")'.format(path))

    def set_font(self, font):
        """Set terminal font via CSS."""
        self.font = font
        self.eval_javascript('fitFont("{0}")'.format(self.font))

    def set_theme(self, theme, color_scheme):
        """Set theme for the terminal."""
        supported_themes = ANSI_COLORS.keys()
        new_theme = {}
        if theme not in supported_themes:
            theme = 'spyder' if color_scheme == 'light' else 'spyder/dark'

        new_theme['background'] = CONF.get('appearance',
                                           '{}/background'.format(theme))
        new_theme['foreground'] = CONF.get('appearance',
                                           '{}/normal'.format(theme))[0]
        new_theme['cursor'] = CONF.get('appearance',
                                       '{}/normal'.format(theme))[0]
        new_theme['cursorAccent'] = CONF.get('appearance',
                                             '{}/ctrlclick'.format(theme))
        new_theme['selection'] = CONF.get('appearance',
                                          '{}/occurrence'.format(theme))
        theme_colors = ANSI_COLORS[theme]
        for color in theme_colors:
            new_theme[color] = theme_colors[color]

        self.eval_javascript('setOption("{}", {})'.format('theme', new_theme))
        self.set_option('fontFamily', CONF.get('appearance', 'font/family'))
        return new_theme

    def get_fonts(self):
        """List terminal CSS fonts."""
        return self.eval_javascript('getFonts()')

    def search_next(self, text, case=False, regex=False, word=False):
        """Search in the terminal for the given regex."""
        search_options = {'regex': regex,
                          'wholeWord': word,
                          'caseSensitive': case}
        return self.eval_javascript(
            'searchNext("{}",{})'.format(text, json.dumps(search_options)))

    def search_previous(self, text, case=False, regex=False, word=False):
        """Search in the terminal for the given regex."""
        search_options = {'regex': regex,
                          'wholeWord': word,
                          'caseSensitive': case}
        return self.eval_javascript(
            'searchPrevious("{}", {})'.format(text,
                                              json.dumps(search_options)))

    def exec_cmd(self, cmd):
        """Execute a command inside the terminal."""
        self.eval_javascript('exec("{0}")'.format(cmd))

    def __alive_loopback(self):
        alive = self.is_alive()
        if not alive:
            self.terminal_closed.emit()
        else:
            QTimer.singleShot(250, self.__alive_loopback)

    def is_alive(self):
        """Check if terminal process is alive."""
        alive = self.eval_javascript('isAlive()')
        return alive

    def set_option(self, option_name, option):
        """Set a configuration option in the terminal."""
        self.eval_javascript('setOption("{}", "{}")'.format(option_name,
                                                            option))

    def apply_settings(self, options):
        """Apply custom settings given an option dictionary."""
        # Bell style option
        if 'sound' in options:
            bell_style = 'sound' if options['sound'] else 'none'
            self.set_option('bellStyle', bell_style)
        # Cursor option
        if 'cursor_type' in options:
            cursor_id = options['cursor_type']
            cursor_choices = {0: "block", 1: "underline", 2: "bar"}
            self.set_option('cursorStyle', cursor_choices[cursor_id])
        if 'color_scheme_name' in options:
            color_scheme = CONF.get('appearance', 'ui_theme')
            theme = CONF.get('appearance', 'selected')
            self.set_theme(theme, color_scheme)


class TermView(QWebEngineView):
    """XTerm Wrapper."""

    def __init__(self, parent, CONF, term_url='http://127.0.0.1:8070',
                 handler=None):
        """Webview main constructor."""
        super().__init__(parent)
        web_page = QWebEnginePage(self)
        self.setPage(web_page)
        self.source_text = ''
        self.parent = parent
        self.CONF = CONF
        self.shortcuts = self.create_shortcuts()
        self.channel = QWebChannel(self.page())
        self.page().setWebChannel(self.channel)
        self.channel.registerObject('handler', handler)

        self.term_url = QUrl(term_url)
        self.load(self.term_url)

        self.document = self.page()
        try:
            self.document.profile().clearHttpCache()
        except AttributeError:
            pass

        self.initial_y_pos = 0
        self.setFocusPolicy(Qt.ClickFocus)

    def copy(self):
        """Copy unicode text from terminal."""
        self.triggerPageAction(QWebEnginePage.Copy)

    def paste(self):
        """Paste unicode text into terminal."""
        clipboard = QApplication.clipboard()
        text = str(clipboard.text())
        if len(text.splitlines()) > 1:
            eol_chars = os.linesep
            text = eol_chars.join((text + eol_chars).splitlines())
        self.eval_javascript('pasteText({})'.format(repr(text)))

    def clear(self):
        """Clear the terminal."""
        self.eval_javascript('clearTerm()')

    def increase_font(self):
        """Increase terminal font."""
        return self.eval_javascript('increaseFontSize()')

    def decrease_font(self):
        """Decrease terminal font."""
        return self.eval_javascript('decreaseFontSize()')

    def create_shortcuts(self):
        """Create the terminal shortcuts."""
        copy_shortcut = self.CONF.config_shortcut(
            lambda: self.copy(),
            context='terminal',
            name='copy',
            parent=self)
        paste_shortcut = self.CONF.config_shortcut(
            lambda: self.paste(),
            context='terminal',
            name='paste',
            parent=self)
        clear_shortcut = self.CONF.config_shortcut(
            lambda: self.clear(),
            context='terminal',
            name='clear',
            parent=self)
        zoomin_shortcut = self.CONF.config_shortcut(
            lambda: self.increase_font(),
            context='terminal',
            name='zoom in',
            parent=self)
        zoomout_shortcut = self.CONF.config_shortcut(
            lambda: self.decrease_font(),
            context='terminal',
            name='zoom out',
            parent=self)
        return [copy_shortcut, paste_shortcut, clear_shortcut, zoomin_shortcut,
                zoomout_shortcut]

    def get_shortcut_data(self):
        """
        Return shortcut data, a list of tuples (shortcut, text, default).

        shortcut (QShortcut or QAction instance)
        text (string): action/shortcut description
        default (string): default key sequence
        """
        return [sc.data for sc in self.shortcuts]

    def contextMenuEvent(self, event):
        """Override Qt method."""
        copy_action = create_action(
            self, _("Copy text"), icon=ima.icon('editcopy'),
            triggered=self.copy,
            shortcut=self.CONF.get_shortcut(CONF_SECTION, 'copy'))
        paste_action = create_action(
            self, _("Paste text"),
            icon=ima.icon('editpaste'),
            triggered=self.paste,
            shortcut=self.CONF.get_shortcut(CONF_SECTION, 'paste'))
        clear_action = create_action(
            self, _("Clear Terminal"),
            triggered=self.clear,
            shortcut=self.CONF.get_shortcut(CONF_SECTION, 'clear'))
        zoom_in = create_action(
            self, _("Zoom in"), triggered=self.increase_font,
            shortcut=self.CONF.get_shortcut(CONF_SECTION, 'zoom in'))
        zoom_out = create_action(
            self, _("Zoom out"), triggered=self.decrease_font,
            shortcut=self.CONF.get_shortcut(CONF_SECTION, 'zoom out'))
        menu = QMenu(self)
        actions = [self.pageAction(QWebEnginePage.SelectAll),
                   copy_action, paste_action, clear_action, None, zoom_in,
                   zoom_out]
        add_actions(menu, actions)
        menu.popup(event.globalPos())
        event.accept()

    def eval_javascript(self, script):
        """
        Evaluate Javascript instructions inside DOM with the expected prefix.
        """
        script = PREFIX + script
        self.document.runJavaScript("{}".format(script), self.return_js_value)

    def return_js_value(self, value):
        """Return the value of the function evaluated in Javascript."""
        return value

    def wheelEvent(self, event):
        """Catch and process wheel scrolling events via Javascript."""
        delta = event.angleDelta().y()
        self.eval_javascript('scrollTerm({0})'.format(delta))

    def event(self, event):
        """Grab all keyboard input."""
        if event.type() == QEvent.ShortcutOverride:
            self.keyPressEvent(event)
            return True
        return True

    def keyPressEvent(self, event):
        """Qt override method."""
        key = event.key()
        modifiers = event.modifiers()

        if modifiers & Qt.ShiftModifier:
            key += Qt.SHIFT
        if modifiers & Qt.ControlModifier:
            key += Qt.CTRL
        if modifiers & Qt.AltModifier:
            key += Qt.ALT
        if modifiers & Qt.MetaModifier:
            key += Qt.META

        sequence = QKeySequence(key).toString(QKeySequence.PortableText)
        if event == QKeySequence.Paste:
            self.paste()
        elif sequence == self.CONF.get_shortcut(CONF_SECTION, 'copy'):
            self.copy()
        elif sequence == self.CONF.get_shortcut(CONF_SECTION, 'paste'):
            self.paste()
        elif sequence == self.CONF.get_shortcut(CONF_SECTION, 'clear'):
            self.clear()
        elif sequence == self.CONF.get_shortcut(
                CONF_SECTION, 'zoom in'):
            self.increase_font()
        elif sequence == self.CONF.get_shortcut(
                CONF_SECTION, 'zoom out'):
            self.decrease_font()
        else:
            super().keyPressEvent(event)


def test():
    """Plugin visual test."""
    from spyder.utils.qthelpers import qapplication
    app = qapplication(test_time=8)
    term = TerminalWidget(None)
    # term.resize(900, 700)
    term.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
