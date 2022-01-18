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
import qstylizer
from qtpy.QtCore import (Qt, QUrl, Slot, QEvent, QTimer, Signal,
                         QObject)
from qtpy.QtGui import QKeySequence
from qtpy.QtWebChannel import QWebChannel
from qtpy.QtWebEngineWidgets import (QWebEnginePage, QWebEngineSettings,
                                     QWebEngineView)
from qtpy.QtWidgets import QFrame, QVBoxLayout, QApplication
from spyder.api.widgets.mixins import SpyderWidgetMixin
from spyder.api.config.decorators import on_conf_change
from spyder.config.base import get_translation
from spyder.config.gui import is_dark_interface
from spyder.utils.palette import QStylePalette

# Local imports
from spyder_terminal.api import TerminalMainWidgetActions, TermViewMenus
from spyder_terminal.widgets.style.themes import ANSI_COLORS


PREFIX = 'spyder_terminal.default.'

# For translations
_ = get_translation('spyder_terminal')


class TermViewSections:
    CommonActions = 'common_actions'
    ZoomActions = 'zoom_actions'


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


class TerminalWidget(QFrame, SpyderWidgetMixin):
    """Terminal widget."""
    ENV_ROUTES = {
        "bash": ["/etc/profile", "~/.bash_profile"],
        "zsh": ["~/.zshrc"],
        "fish": ["~/.config/fish/config.fish"],
        "sh": ["~/.profile", "~/.shrc", "~/.shinit"],
        "ksh": ["~/.profile", "~/.kshrc"],
        "csh": ["~/.cshrc", "~/.login"],
        "pwsh": [],
        "rbash": ["~/.bashrc", "~/.bash_profile"],
        "dash": ["~/.profile"],
        "screen": [],
        "tmux": [],
        "tcsh": ["~/.tcshrc"],
        "xonsh": ["~/.xonshrc"]
    }

    terminal_closed = Signal()
    terminal_ready = Signal()

    def __init__(self, parent, port, path='~', font=None, theme=None,
                 color_scheme=None):
        """Frame main constructor."""
        super().__init__(parent, class_parent=parent)
        url = 'http://127.0.0.1:{0}?path={1}'.format(port, path)
        self.handler = ChannelHandler(self)
        self.handler.sig_ready.connect(lambda: self.terminal_ready.emit())
        self.handler.sig_closed.connect(lambda: self.terminal_closed.emit())
        self.view = TermView(self, term_url=url, handler=self.handler)
        self.font = font
        self.initial_path = path
        self.theme = theme
        self.color_scheme = color_scheme
        self.parent = parent
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.NoFrame | QFrame.Plain)
        self.setLayout(layout)

        self.body = self.view.document

        self.handler.sig_ready.connect(self.setup_term)
        self.view.sig_focus_in_event.connect(
            lambda: self._apply_stylesheet(focus=True))
        self.view.sig_focus_out_event.connect(
            lambda: self._apply_stylesheet(focus=False))
        self._apply_stylesheet()

    def setup_term(self):
        """Setup other terminal options after page has loaded."""
        # This forces to display the black background
        print("\0", end='')
        self.set_font(self.font)
        self.set_dir(self.initial_path)
        self.current_theme = self.set_theme({})
        self.set_scrollbar_style()
        options = self.get_conf_options()
        dict_options = {}
        for option in options:
            dict_options[option] = self.get_conf(option)
        self.apply_settings(dict_options)
        self.apply_zoom()
        shell_name = self.get_conf('shell')
        if os.name != 'nt':
            # Find environment variables in the home directory given the actual
            # shell
            env_route = self.ENV_ROUTES[shell_name]
            for act_file in env_route:
                if os.path.exists(os.path.expanduser(act_file)):
                    self.exec_cmd(f"source {act_file}")
                    self.exec_cmd("clear")

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

    @on_conf_change(section='appearance')
    def set_theme(self, _values):
        """Set theme for the terminal."""
        supported_themes = ANSI_COLORS
        new_theme = {}
        theme = self.get_conf('selected', section='appearance')
        color_scheme = self.get_conf('ui_theme', section='appearance')
        if theme not in supported_themes:
            theme = 'spyder' if color_scheme == 'light' else 'spyder/dark'
        new_theme['background'] = self.get_conf(
            '{}/background'.format(theme), section='appearance')
        new_theme['foreground'] = self.get_conf(
            '{}/normal'.format(theme), section='appearance')[0]
        new_theme['cursor'] = self.get_conf(
            '{}/normal'.format(theme), section='appearance')[0]
        new_theme['cursorAccent'] = self.get_conf(
            '{}/ctrlclick'.format(theme), section='appearance')
        new_theme['selection'] = self.get_conf(
            '{}/occurrence'.format(theme), section='appearance')
        theme_colors = ANSI_COLORS[theme]
        for color in theme_colors:
            new_theme[color] = theme_colors[color]

        self.eval_javascript('setOption("{}", {})'.format('theme', new_theme))
        self.set_conf(
            'fontFamily', self.get_conf('font/family', section='appearance'))
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

    def apply_zoom(self):
        zoom = self.get_conf('zoom')
        if zoom > 0:
            for __ in range(0, zoom):
                self.view.increase_font()
        if zoom < 0:
            for __ in range(0, -zoom):
                self.view.decrease_font()

    def set_option(self, option_name, option):
        """Set a configuration option in the terminal."""
        if type(option) == int:
            self.eval_javascript('setOption("{}", {})'.format(option_name,
                                                              option))
        else:
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
        if 'buffer_limit' in options:
            new_lim = options['buffer_limit']
            self.set_option('scrollback', new_lim)
        if 'cursor_blink' in options:
            self.set_option('cursorBlink', int(options['cursor_blink']))

    def _apply_stylesheet(self, focus=False):
        """Apply stylesheet according to the current focus."""
        if focus:
            border_color = QStylePalette.COLOR_ACCENT_3
        else:
            border_color = QStylePalette.COLOR_BACKGROUND_4

        css = qstylizer.style.StyleSheet()
        css.QFrame.setValues(
            border=f'1px solid {border_color}',
            margin='0px 1px 0px 1px',
            padding='0px 0px 1px 0px',
            borderRadius='3px'
        )

        self.setStyleSheet(css.toString())


class TermView(QWebEngineView, SpyderWidgetMixin):
    """XTerm Wrapper."""
    sig_focus_in_event = Signal()
    """
    This signal is emitted when the widget receives focus.
    """

    sig_focus_out_event = Signal()
    """
    This signal is emitted when the widget loses focus.
    """

    def __init__(self, parent, term_url='http://127.0.0.1:8070', handler=None):
        """Webview main constructor."""
        super().__init__(parent, class_parent=parent)
        web_page = QWebEnginePage(self)
        self.setPage(web_page)
        self.source_text = ''
        self.parent = parent
        self.channel = QWebChannel(self.page())
        self.page().setWebChannel(self.channel)
        self.channel.registerObject('handler', handler)

        self.term_url = QUrl(term_url)
        self.load(self.term_url)
        self.focusProxy().installEventFilter(self)

        self.document = self.page()
        try:
            self.document.profile().clearHttpCache()
        except AttributeError:
            pass

        self.initial_y_pos = 0
        self.setFocusPolicy(Qt.ClickFocus)
        self.setup()

    def setup(self):
        """Create the terminal context menu."""
        # Create context menu
        self.context_menu = self.get_menu(TermViewMenus.Context)
        for item in [self.get_action(TerminalMainWidgetActions.Copy),
                     self.get_action(TerminalMainWidgetActions.Paste),
                     self.get_action(TerminalMainWidgetActions.Clear)]:
            self.add_item_to_menu(
                item,
                menu=self.context_menu,
                section=TermViewSections.CommonActions,
            )

        for item in [self.get_action(TerminalMainWidgetActions.ZoomIn),
                     self.get_action(TerminalMainWidgetActions.ZoomOut)]:
            self.add_item_to_menu(
                item,
                menu=self.context_menu,
                section=TermViewSections.ZoomActions,
            )

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
        zoom = self.get_conf('zoom')
        self.set_conf('zoom', zoom + 1)
        return self.eval_javascript('increaseFontSize()')

    def decrease_font(self):
        """Decrease terminal font."""
        zoom = self.get_conf('zoom')
        self.set_conf('zoom', zoom - 1)
        return self.eval_javascript('decreaseFontSize()')

    def contextMenuEvent(self, event):
        """Override Qt method."""
        self.context_menu.popup(event.globalPos())
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
        elif sequence == self.get_shortcut('copy'):
            self.copy()
        elif sequence == self.get_shortcut('paste'):
            self.paste()
        elif sequence == self.get_shortcut('clear'):
            self.clear()
        elif sequence == self.get_shortcut('zoom_in'):
            self.increase_font()
        elif sequence == self.get_shortcut('zoom_out'):
            self.decrease_font()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, widget, event):
        """
        Handle events that affect the view.
        All events (e.g. focus in/out) reach the focus proxy, not this
        widget itself. That's why this event filter is necessary.
        """
        if self.focusProxy() is widget:
            if event.type() == QEvent.FocusIn:
                self.sig_focus_in_event.emit()
            elif event.type() == QEvent.FocusOut:
                self.sig_focus_out_event.emit()
        return super().eventFilter(widget, event)


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
