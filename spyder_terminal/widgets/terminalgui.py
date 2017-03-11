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
from qtpy.QtWidgets import (QVBoxLayout, QWidget)
from spyder.widgets.browser import WebView


class TerminalWidget(QWidget):
    """Terminal widget."""
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.view = TermView(self)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)


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
