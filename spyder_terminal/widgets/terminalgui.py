# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Terminal Widget."""

import sys

from spyder.config.base import _
from qtpy.QtCore import Qt, QUrl, Signal, Slot
from spyder.config.gui import config_shortcut
from qtpy.QtWidgets import (QMenu, QFrame, QVBoxLayout, QWidget, QShortcut)
from qtpy.QtGui import QKeySequence
from spyder.widgets.browser import WebView
from spyder.utils import icon_manager as ima
from qtpy.QtWebEngineWidgets import QWebEnginePage
from spyder.utils.qthelpers import create_action, add_actions

from qtpy.QtWebEngineWidgets import WEBENGINE


class TerminalWidget(QFrame):
    """Terminal widget."""

    def __init__(self, parent, font=None):
        """Frame main constructor."""
        QWidget.__init__(self, parent)
        self.view = TermView(self, font=font)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLayout(layout)

        if WEBENGINE:
            self.body = self.view.page()
        else:
            self.body = self.view.page().mainFrame()


class TermView(WebView):
    """XTerm Wrapper."""

    def __init__(self, parent, term_url='http://127.0.0.1:8070', font=None):
        """Webview main constructor."""
        WebView.__init__(self, parent)
        self.copy_action = create_action(self, _("Copy text"),
                                         icon=ima.icon('editcopy'),
                                         triggered=self.copy,
                                         shortcut='Ctrl+Alt+C')
        self.paste_action = create_action(self, _("Paste text"),
                                          icon=ima.icon('editpaste'),
                                          triggered=self.paste,
                                          shortcut='Ctrl+Alt+V')
        self.term_url = QUrl(term_url)
        self.load(self.term_url)
        copy_shortcut = QShortcut(QKeySequence("Ctrl+Alt+C"),
                                  self, self.copy)
        copy_shortcut.setContext(Qt.WidgetWithChildrenShortcut)

        paste_shortcut = QShortcut(QKeySequence("Ctrl+Alt+V"),
                                   self, self.paste)
        paste_shortcut.setContext(Qt.WidgetWithChildrenShortcut)

    def copy(self):
        """Copy unicode text from terminal."""
        self.triggerPageAction(QWebEnginePage.Copy)

    def paste(self):
        """Paste unicode text into terminal."""
        self.triggerPageAction(QWebEnginePage.Paste)

    def contextMenuEvent(self, event):
        """Override Qt method."""
        menu = QMenu(self)
        actions = [self.pageAction(QWebEnginePage.SelectAll),
                   self.copy_action, self.paste_action, None,
                   self.zoom_in_action, self.zoom_out_action]
        add_actions(menu, actions)
        menu.popup(event.globalPos())
        event.accept()


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
