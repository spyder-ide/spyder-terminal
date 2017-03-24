# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Terminal Widget."""

import sys
from qtpy.QtCore import QUrl, Signal, Slot
from spyder.config.gui import config_shortcut
from qtpy.QtWidgets import (QVBoxLayout, QWidget)
from spyder.widgets.browser import WebView
from qtpy.QtWebEngineWidgets import QWebEnginePage


class TerminalWidget(QWidget):
    """Terminal widget."""
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.view = TermView(self)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.shortcuts = self.create_shortcuts()

    def create_shortcuts(self):
        copy = config_shortcut(self.copy, context='Terminal',
                               name='Copy text from terminal', parent=self)
        paste = config_shortcut(self.paste, context='Terminal',
                                name='Paste text into terminal',
                                parent=self)
        return [copy, paste]

    def copy(self):
        self.view.triggerPageAction(QWebEnginePage.Copy)

    def paste(self):
        self.view.triggerPageAction(QWebEnginePage.Paste)


class TermView(WebView):
    """XTerm Wrapper"""
    def __init__(self, parent, term_url='http://127.0.0.1:8000'):
        WebView.__init__(self, parent)
        self.term_url = QUrl(term_url)
        self.load(self.term_url)


def test():
    from spyder.utils.qthelpers import qapplication
    app = qapplication(test_time=8)
    term = TerminalWidget(None)
    # term.resize(900, 700)
    term.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
