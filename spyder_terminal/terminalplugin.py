# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Terminal Plugin."""

import os
import sys
import time
import subprocess
import os.path as osp

from qtpy.QtWidgets import QApplication, QMessageBox, QVBoxLayout, QMenu
from qtpy.QtCore import Qt, Signal

from spyder.plugins import SpyderPluginWidget

# from spyder.preferences import PluginConfigPage

from spyder.config.base import _
from spyder.utils import icon_manager as ima
from spyder.utils.qthelpers import (create_action, create_toolbutton,
                                    add_actions)
from spyder.widgets.tabs import Tabs
# from spyder.plugins import SpyderPluginWidget

from spyder_terminal.widgets.terminalgui import TerminalWidget


LOCATION = osp.realpath(osp.join(os.getcwd(),
                                 osp.dirname(__file__)))

# class TerminalConfigPage(PluginConfigPage):
#     """Terminal plugin preferences."""
#     pass


class TerminalPlugin(SpyderPluginWidget):
    """Terminal plugin."""
    CONF_SECTION = 'terminal'
    focus_changed = Signal()

    def __init__(self, parent):
        SpyderPluginWidget.__init__(self, parent)
        self.tab_widget = None
        self.menu_actions = None
        self.server = subprocess.Popen(
            ['python', osp.join(LOCATION, 'server', 'main.py')],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        time.sleep(0.5)
        self.main = parent

        self.terms = []
        self.untitled_num = 0
        self.initialize_plugin()

        layout = QVBoxLayout()
        new_term_btn = create_toolbutton(self,
                                         icon=ima.icon('project_expanded'),
                                         tip=_('Open a new terminal'),
                                         triggered=self.create_new_term)
        menu_btn = create_toolbutton(self, icon=ima.icon('tooloptions'),
                                     tip=_('Options'))
        self.menu = QMenu(self)
        menu_btn.setMenu(self.menu)
        menu_btn.setPopupMode(menu_btn.InstantPopup)
        add_actions(self.menu, self.menu_actions)
        corner_widgets = {Qt.TopRightCorner: [new_term_btn, menu_btn]}
        self.tabwidget = Tabs(self, menu=self.menu, actions=self.menu_actions,
                              corner_widgets=corner_widgets)
        if hasattr(self.tabwidget, 'setDocumentMode') \
           and not sys.platform == 'darwin':
            # Don't set document mode to true on OSX because it generates
            # a crash when the console is detached from the main window
            # Fixes Issue 561
            self.tabwidget.setDocumentMode(True)
        self.tabwidget.currentChanged.connect(self.refresh_plugin)
        self.tabwidget.move_data.connect(self.move_tab)

        self.tabwidget.set_close_function(self.close_term)

        layout.addWidget(self.tabwidget)
        self.setLayout(layout)

    # ------ SpyderPluginMixin API --------------------------------
    def on_first_registration(self):
        """Action to be performed on first plugin registration"""
        self.main.tabify_plugins(self.main.extconsole, self)

    def update_font(self):
        """Update font from Preferences"""
        pass

    # ------ SpyderPluginWidget API ------------------------------
    def get_plugin_title(self):
        """Return widget title"""
        title = _('System Terminal')
        return title

    def get_plugin_icon(self):
        """Return widget icon"""
        return ima.icon('cmdprompt')

    def get_plugin_actions(self):
        self.menu_actions = []
        return self.menu_actions

    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        term = self.tabwidget.currentWidget()
        if term is not None:
            return term.view

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        for term in self.terms:
            term.close()
        self.server.terminate()
        return True

    def refresh_plugin(self):
        """Refresh tabwidget"""
        term = None
        if self.tabwidget.count():
            term = self.tabwidget.currentWidget()
            term.view.setFocus()
        else:
            term = None

    def register_plugin(self):
        """Register plugin in Spyder's main window"""
        # print("Am I being called?")
        self.focus_changed.connect(self.main.plugin_focus_changed)
        self.main.add_dockwidget(self)
        self.create_new_term(give_focus=False)

    # ------ Public API (for terminals) -------------------------
    def get_terms(self):
        """Return terminal list"""
        return [cl for cl in self.terms if isinstance(cl, TerminalWidget)]

    def get_focus_term(self):
        """Return current terminal with focus, if any"""
        widget = QApplication.focusWidget()
        for term in self.get_terms():
            if widget is term:
                return term

    def get_current_term(self):
        """Return the currently selected terminal"""
        try:
            terminal = self.tabwidget.currentWidget()
        except AttributeError:
            terminal = None
        if terminal is not None:
            return terminal

    def create_new_term(self, name=None, give_focus=True):
        term = TerminalWidget(self)
        self.add_tab(term)

    def close_term(self, index=None, term=None):
        if not self.tabwidget.count():
            return
        if term is not None:
            index = self.tabwidget.indexOf(term)
        if index is None and term is None:
            index = self.tabwidget.currentIndex()
        if index is not None:
            term = self.tabwidget.widget(index)

        term.close()
        self.tabwidget.removeTab(self.tabwidget.indexOf(term))
        self.terms.remove(term)

    # ------ Public API (for tabs) ---------------------------
    def add_tab(self, widget):
        """Add tab"""
        self.terms.append(widget)
        index = self.tabwidget.addTab(widget, "Terminal")
        self.tabwidget.setCurrentIndex(index)
        self.tabwidget.setTabToolTip(index, "Terminal")
        if self.dockwidget and not self.ismaximized:
            self.dockwidget.setVisible(True)
            self.dockwidget.raise_()
        self.activateWindow()
        widget.view.setFocus()

    def move_tab(self, index_from, index_to):
        """
        Move tab (tabs themselves have already been moved by the tabwidget)
        """
        term = self.terms.pop(index_from)
        self.terms.insert(index_to, term)
