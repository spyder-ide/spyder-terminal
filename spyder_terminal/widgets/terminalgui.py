# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Terminal Widget."""

import os
import sys
import subprocess
from qtpy.QtCore import QUrl, Signal, Slot
from qtpy.QtWidgets import (QFrame, QHBoxLayout, QLabel, QProgressBar, QMenu,
                            QVBoxLayout, QWidget)
from qtpy.QtWebEngineWidgets import WEBENGINE
from spyder.widgets.browser import WebView, WebPage
# from PyQt5.QtWebChannel import QWebChannel


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
        # QWebEngineView.__init__(self, parent)
        print(WEBENGINE)
        # self.zoom_factor = 1.
        self.num_cols = 24
        self.num_rows = 13
        self.term_url = QUrl(term_url)
        # self.channel = QWebChannel(self.page())
        # page = WebPage(self)
        # page.setWebChannel(self.channel)
        # self.setPage(page)
        # print(type(self.))
        self.load(self.term_url)


def test():
    from spyder.utils.qthelpers import qapplication
    # from spyder.config.base import get_module_path
    # from spyder.utils.introspection.manager import IntrospectionManager

    # cur_dir = osp.join(get_module_path('spyder'), 'widgets')
    app = qapplication(test_time=8)
    term = TerminalWidget(None)
    term.show()
    # introspector = IntrospectionManager()

    # test = EditorPluginExample()
    # test.resize(900, 700)
    # test.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
