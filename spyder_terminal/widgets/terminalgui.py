# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Terminal Widget."""

import os
import subprocess
from qtpy.QtCore import QUrl, Signal, Slot
from qtpy.QtWidgets import (QFrame, QHBoxLayout, QLabel, QProgressBar, QMenu,
                            QVBoxLayout, QWidget)
from qtpy.QtWebEngineWidgets import (QWebEnginePage, QWebEngineSettings,
                                     QWebEngineView, WEBENGINE)



class TerminalWidget(QWidget):
    """Terminal widget."""
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.view = TermView(self)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)


class TermView(QWebEngineView):
    """XTerm Wrapper"""
    def __init__(self, parent):
        QWebEngineView.__init__(self, parent)
        self.zoom_factor = 1.

    def createWindow(self, webwindowtype):
        import webbrowser
        webbrowser.open(to_text_string(self.url().toString()))

    def setHtml(self, html, baseUrl=QUrl()):
        """
        Reimplement Qt method to prevent WebEngine to steal focus
        when setting html on the page

        Solution taken from
        https://bugreports.qt.io/browse/QTBUG-52999
        """
        if WEBENGINE:
            self.setEnabled(False)
            super(TermView, self).setHtml(html, baseUrl)
            self.setEnabled(True)
        else:
            super(TermView, self).setHtml(html, baseUrl)


def test():
    from spyder.utils.qthelpers import qapplication
    # from spyder.config.base import get_module_path
    # from spyder.utils.introspection.manager import IntrospectionManager

    # cur_dir = osp.join(get_module_path('spyder'), 'widgets')
    app = qapplication(test_time=8)
    
    # introspector = IntrospectionManager()

    # test = EditorPluginExample()
    test.resize(900, 700)
    test.show()


    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
