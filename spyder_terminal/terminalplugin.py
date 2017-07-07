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
import requests
import subprocess
import os.path as osp

from qtpy import PYQT4, PYSIDE
from qtpy.QtWidgets import (QApplication, QMessageBox, QVBoxLayout, QMenu,
                            QShortcut)

from qtpy.QtCore import Qt, Signal, QTimer, Slot
from qtpy.QtGui import QKeySequence

from spyder.plugins import SpyderPluginWidget

# from spyder.preferences import PluginConfigPage

from spyder.config.base import _
from spyder.utils import icon_manager as ima
from spyder.utils.programs import find_program
from spyder.utils.qthelpers import (create_action, create_toolbutton,
                                    add_actions)
from spyder.widgets.tabs import Tabs
# from spyder.config.gui import set_shortcut, config_shortcut
# from spyder.plugins import SpyderPluginWidget

from spyder_terminal.widgets.terminalgui import TerminalWidget
# from spyder.py3compat import is_text_string, to_text_string
from spyder.utils.misc import select_port

from spyder.py3compat import PY2, getcwd
from spyder.config.base import DEV

LOCATION = osp.realpath(osp.join(os.getcwd(),
                                 osp.dirname(__file__)))
WINDOWS = os.name == 'nt'

# class TerminalConfigPage(PluginConfigPage):
#     """Terminal plugin preferences."""
#     pass


class TerminalPlugin(SpyderPluginWidget):
    """Terminal plugin."""

    URL_ISSUES = ' https://github.com/spyder-ide/spyder-terminal/issues'
    CONF_SECTION = 'terminal'
    focus_changed = Signal()
    MAX_SERVER_CONTACT_RETRIES = 40

    def __init__(self, parent):
        """Widget constructor."""
        SpyderPluginWidget.__init__(self, parent)
        self.tab_widget = None
        self.menu_actions = None
        self.server_retries = 0
        self.port = select_port(default_port=8071)

        self.cmd = '/usr/bin/env bash'
        if WINDOWS:
            self.cmd = find_program('cmd.exe')

        self.server_stdout = subprocess.PIPE
        self.server_stderr = subprocess.PIPE
        self.stdout_file = osp.join(getcwd(), 'spyder_terminal_out.log')
        self.stderr_file = osp.join(getcwd(), 'spyder_terminal_err.log')
        if DEV:
            self.server_stdout = open(self.stdout_file, 'w')
            self.server_stderr = open(self.stderr_file, 'w')

        self.server = subprocess.Popen(
            [sys.executable, osp.join(LOCATION, 'server', 'main.py'),
             '--port', str(self.port), '--shell', self.cmd],
            stdout=self.server_stdout,
            stderr=self.server_stderr)

        self.main = parent

        self.terms = []
        self.untitled_num = 0

        self.project_path = None
        self.current_file_path = None
        self.current_cwd = getcwd()

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
        # if self.get_option('first_time', True):
        # self.setup_shortcuts()
        # self.shortcuts = self.create_shortcuts()
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

        new_term_shortcut = QShortcut(QKeySequence("Ctrl+Alt+Shift+T"),
                                      self, self.create_new_term)
        new_term_shortcut.setContext(Qt.WidgetWithChildrenShortcut)

        self.__wait_server_to_start()

    # ------ Private API ------------------------------------------
    def __wait_server_to_start(self):
        try:
            code = requests.get('http://127.0.0.1:{0}'.format(
                self.port)).status_code
        except:
            code = 500

        if self.server_retries == self.MAX_SERVER_CONTACT_RETRIES:
            QMessageBox.Critical(self, _('Spyder Terminal Error'),
                                 _("Terminal server could not be located at "
                                   '<a href="http://127.0.0.1:{0}">'
                                   'http://127.0.0.1:{0}</a>,'
                                   ' please restart Spyder on debugging mode '
                                   "and open an issue with the contents of "
                                   "<tt>{1}</tt> and <tt>{2}</tt> "
                                   "files at {3}.").format(self.port,
                                                           self.stdout_file,
                                                           self.stderr_file,
                                                           self.URL_ISSUES),
                                 QMessageBox.Ok)
        elif code != 200:
            self.server_retries += 1
            QTimer.singleShot(250, self.__wait_server_to_start)
        elif code == 200:
            self.create_new_term(give_focus=False)

    # ------ SpyderPluginMixin API --------------------------------
    def on_first_registration(self):
        """Action to be performed on first plugin registration."""
        self.main.tabify_plugins(self.main.ipyconsole, self)

    def update_font(self):
        """Update font from Preferences."""
        font = self.get_plugin_font()
        for term in self.terms:
            term.set_font(font.family())

    def check_compatibility(self):
        """Check if current Qt backend version is greater or equal to 5."""
        message = ''
        valid = True
        if PYQT4 or PYSIDE:
            message = 'This plugin does not work with Qt 4'
            valid = False
        elif WINDOWS and PY2:
            message = 'This plugin does not work with Python 2 on Windows'
            valid = False
        return valid, message

    # ------ SpyderPluginWidget API ------------------------------
    def get_plugin_title(self):
        """Return widget title."""
        title = _('Terminal')
        return title

    def get_plugin_icon(self):
        """Return widget icon."""
        return ima.icon('cmdprompt')

    def get_plugin_actions(self):
        """Get plugin actions."""
        new_terminal_cwd = create_action(self,
                                         _("New terminal in current "
                                           "working directory"),
                                         tip=_("Sets the pwd at "
                                               "the current workind "
                                               "directory"),
                                         triggered=self.create_new_term)

        self.new_terminal_project = create_action(self,
                                                  _("New terminal in current "
                                                    "project"),
                                                  tip=_("Sets the pwd at "
                                                        "the current project "
                                                        "directory"),
                                                  triggered=lambda:
                                                  self.create_new_term(
                                                      path=self.project_path))

        if self.project_path is None:
            self.new_terminal_project.setEnabled(False)

        new_terminal_file = create_action(self,
                                          _("New terminal in current Editor "
                                            "file"),
                                          tip=_("Sets the pwd at "
                                                "the directory that contains "
                                                "the current opened file"),
                                          triggered=lambda:
                                          self.create_new_term(
                                              path=self.current_file_path))

        self.menu_actions = [new_terminal_cwd, self.new_terminal_project,
                             new_terminal_file]
        return self.menu_actions

    def get_focus_widget(self):
        """
        Set focus on current selected terminal.

        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level.
        """
        term = self.tabwidget.currentWidget()
        if term is not None:
            return term.view

    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed."""
        for term in self.terms:
            term.close()
        self.server.terminate()
        if DEV:
            self.server_stdout.close()
            self.server_stderr.close()
        return True

    def refresh_plugin(self):
        """Refresh tabwidget."""
        term = None
        if self.tabwidget.count():
            term = self.tabwidget.currentWidget()
            term.view.setFocus()
        else:
            term = None

    def register_plugin(self):
        """Register plugin in Spyder's main window."""
        self.focus_changed.connect(self.main.plugin_focus_changed)
        self.main.add_dockwidget(self)
        self.main.workingdirectory.set_explorer_cwd.connect(
            self.set_current_cwd)
        self.main.projects.sig_project_loaded.connect(self.set_project_path)
        self.main.projects.sig_project_closed.connect(self.unset_project_path)
        self.main.editor.open_file_update.connect(self.set_current_opened_file)

    # ------ Public API (for terminals) -------------------------
    def get_terms(self):
        """Return terminal list."""
        return [cl for cl in self.terms if isinstance(cl, TerminalWidget)]

    def get_focus_term(self):
        """Return current terminal with focus, if any."""
        widget = QApplication.focusWidget()
        for term in self.get_terms():
            if widget is term:
                return term

    def get_current_term(self):
        """Return the currently selected terminal."""
        try:
            terminal = self.tabwidget.currentWidget()
        except AttributeError:
            terminal = None
        if terminal is not None:
            return terminal

    def create_new_term(self, name=None, give_focus=True, path=None):
        """Add a new terminal tab."""
        if path is None:
            path = self.current_cwd
        path = path.replace('\\', '/')
        font = self.get_plugin_font()
        term = TerminalWidget(self, self.port, path=path,
                              font=font.family())
        self.add_tab(term)

    def close_term(self, index=None, term=None):
        """Close a terminal tab."""
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
        if self.tabwidget.count() == 0:
            self.create_new_term()

    def set_project_path(self, path):
        """Refresh current project path."""
        self.project_path = path
        self.new_terminal_project.setEnabled(True)

    def set_current_opened_file(self, path):
        """Get path of current opened file in editor."""
        self.current_file_path = osp.dirname(path)

    def unset_project_path(self):
        """Refresh current project path."""
        self.project_path = None
        self.new_terminal_project.setEnabled(False)

    @Slot(str)
    def set_current_cwd(self, cwd):
        """Update current working directory."""
        self.current_cwd = cwd

    # ------ Public API (for tabs) ---------------------------
    def add_tab(self, widget):
        """Add tab."""
        self.terms.append(widget)
        num_term = self.tabwidget.count() + 1
        index = self.tabwidget.addTab(widget, "Terminal {0}".format(num_term))
        self.tabwidget.setCurrentIndex(index)
        self.tabwidget.setTabToolTip(index, "Terminal {0}".format(num_term))
        if self.dockwidget and not self.ismaximized:
            self.dockwidget.setVisible(True)
            self.dockwidget.raise_()
        self.activateWindow()
        widget.view.setFocus()

    def move_tab(self, index_from, index_to):
        """
        Move tab (tabs themselves have already been moved by the tabwidget).

        Allows to change order of tabs.
        """
        term = self.terms.pop(index_from)
        self.terms.insert(index_to, term)
