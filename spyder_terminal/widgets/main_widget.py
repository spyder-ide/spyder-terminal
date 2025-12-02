# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Terminal Plugin."""

# Standard imports
import functools
import os
import os.path as osp
import requests
import sys

# Third party imports
import qstylizer
from qtpy.QtCore import QProcess, QTimer, Signal, Slot
from qtpy.QtWidgets import QMessageBox, QVBoxLayout
from spyder.api.config.decorators import on_conf_change
from spyder.api.widgets.main_widget import PluginMainWidget
from spyder.config.base import get_translation, get_debug_level
from spyder.utils.misc import select_port
from spyder.utils.programs import find_program
from spyder.widgets.tabs import Tabs
from spyder.plugins.remoteclient.widgets import AuthenticationMethod

# Local imports
from spyder_terminal.api import (
    TerminalMainWidgetActions,
    TermViewMenus,
    TerminalMainWidgetMenus,
)
from spyder_terminal.widgets.findwidget import FindTerminal
from spyder_terminal.widgets.terminalgui import TerminalWidget


# Constants
LOCATION = osp.realpath(osp.join(os.getcwd(), osp.dirname(__file__)))
WINDOWS = os.name == "nt"

# For translations
_ = get_translation("spyder_terminal")


class TerminalMainWidgetToolbarSections:
    New = "new"
    Reload = "reload"


class TerminalMainWidgetCornerToolbar:
    NewTerm = "new_terminal"


class TerminalMainWidgetMenuSections:
    New = "new"
    TabActions = "tab_actions"


class TerminalMainWidget(PluginMainWidget):
    """
    Terminal plugin main widget.
    """

    MAX_SERVER_CONTACT_RETRIES = 40
    URL_ISSUES = " https://github.com/spyder-ide/spyder-terminal/issues"

    # --- Signals
    # ------------------------------------------------------------------------
    sig_server_is_ready = Signal()
    """
    This signal is emitted when the server is ready to connect.
    """

    def __init__(self, name, plugin, parent):
        """Widget constructor."""
        self.terms = []
        super().__init__(name, plugin, parent)

        # Attributes
        self.tab_widget = None
        self.menu_actions = None
        self.server_retries = 0
        self.server_ready = False
        self.font = None
        self.port = select_port(default_port=8071)
        self.stdout_file = None
        self.stderr_file = None
        if get_debug_level() > 0:
            self.stdout_file = osp.join(os.getcwd(), "spyder_terminal_out.log")
            self.stderr_file = osp.join(os.getcwd(), "spyder_terminal_err.log")
        self.project_path = None
        self.current_file_path = None
        self.current_cwd = os.getcwd()
        self.closing = False

        # Widgets
        self.main = parent
        self.find_widget = FindTerminal(self)
        self.find_widget.hide()

        layout = QVBoxLayout()

        # Tab Widget
        self.tabwidget = Tabs(self, rename_tabs=True)
        self.tabwidget.currentChanged.connect(self.refresh_plugin)
        self.tabwidget.move_data.connect(self.move_tab)
        self.tabwidget.set_close_function(self.close_term)

        if (
            hasattr(self.tabwidget, "setDocumentMode")
            and not sys.platform == "darwin"
        ):
            # Don't set document mode to true on OSX because it generates
            # a crash when the console is detached from the main window
            # Fixes Issue 561
            self.tabwidget.setDocumentMode(True)
        layout.addWidget(self.tabwidget)
        layout.addWidget(self.find_widget)
        self.setLayout(layout)

        css = qstylizer.style.StyleSheet()
        css.QTabWidget.pane.setValues(border=0)
        self.setStyleSheet(css.toString())

        self.__wait_server_to_start()

    # ---- PluginMainWidget API
    # ------------------------------------------------------------------------
    def get_focus_widget(self):
        """
        Set focus on current selected terminal.

        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level.
        """
        term = self.tabwidget.currentWidget()
        if term is not None:
            return term.view

    def get_title(self):
        """Define the title of the widget."""
        return _("Terminal")

    def setup(self):
        """Perform the setup of plugin's main menu and signals."""
        self.cmd = find_program(self.get_conf("shell"))
        server_args = [
            sys.executable,
            "-m",
            "spyder_terminal.server",
            "--port",
            str(self.port),
            "--shell",
            self.cmd,
        ]
        self.server = QProcess(self)
        env = self.server.processEnvironment()
        for var in os.environ:
            env.insert(var, os.environ[var])
        self.server.setProcessEnvironment(env)
        self.server.errorOccurred.connect(self.handle_process_errors)
        self.server.setProcessChannelMode(QProcess.SeparateChannels)
        if self.stdout_file and self.stderr_file:
            self.server.setStandardOutputFile(self.stdout_file)
            self.server.setStandardErrorFile(self.stderr_file)
        self.server.start(server_args[0], server_args[1:])
        self.color_scheme = self.get_conf("appearance", "ui_theme")
        self.theme = self.get_conf("appearance", "selected")

        # Menu
        menu = self.get_options_menu()

        # Actions
        new_terminal_toolbar_action = self.create_toolbutton(
            TerminalMainWidgetToolbarSections.New,
            text=_("Open a new terminal"),
            icon=self.create_icon("expand_selection"),
            triggered=lambda: self.create_new_term(),
        )
        reload_terminal_toolbar_action = self.create_toolbutton(
            TerminalMainWidgetToolbarSections.Reload,
            text=_("Reload terminal"),
            icon=self.create_icon("restart"),
            triggered=lambda: self.reload_current_term(),
        )

        for toolbar_action in [
            new_terminal_toolbar_action,
            reload_terminal_toolbar_action,
        ]:
            self.add_corner_widget(toolbar_action)

        new_terminal_cwd = self.create_action(
            TerminalMainWidgetActions.NewTerminalForCWD,
            text=_("New terminal in current working directory"),
            tip=_("Sets the pwd at the current working directory"),
            triggered=lambda: self.create_new_term(),
            shortcut_context="terminal",
            register_shortcut=True,
        )

        self.new_terminal_project = self.create_action(
            TerminalMainWidgetActions.NewTerminalForProject,
            text=_("New terminal in current project"),
            tip=_("Sets the pwd at the current project directory"),
            triggered=lambda: self.create_new_term(path=self.project_path),
        )

        new_terminal_file = self.create_action(
            TerminalMainWidgetActions.NewTerminalForFile,
            text=_("New terminal in current Editor file"),
            tip=_(
                "Sets the pwd at the directory that contains the current "
                "opened file"
            ),
            triggered=lambda: self.create_new_term(
                path=self.current_file_path
            ),
        )

        rename_tab_action = self.create_action(
            TerminalMainWidgetActions.RenameTab,
            text=_("Rename terminal"),
            triggered=lambda: self.tab_name_editor(),
        )

        # Context menu actions
        self.create_action(
            TerminalMainWidgetActions.Copy,
            text=_("Copy text"),
            icon=self.create_icon("editcopy"),
            shortcut_context="terminal",
            triggered=lambda: self.copy(),
            register_shortcut=True,
        )

        self.create_action(
            TerminalMainWidgetActions.Paste,
            text=_("Paste text"),
            icon=self.create_icon("editpaste"),
            shortcut_context="terminal",
            triggered=lambda: self.paste(),
            register_shortcut=True,
        )

        self.create_action(
            TerminalMainWidgetActions.Clear,
            text=_("Clear terminal"),
            shortcut_context="terminal",
            triggered=lambda: self.clear(),
            register_shortcut=True,
        )

        self.create_action(
            TerminalMainWidgetActions.ZoomIn,
            text=_("Zoom in"),
            shortcut_context="terminal",
            triggered=lambda: self.increase_font(),
            register_shortcut=True,
        )

        self.create_action(
            TerminalMainWidgetActions.ZoomOut,
            text=_("Zoom out"),
            shortcut_context="terminal",
            triggered=lambda: self.decrease_font(),
            register_shortcut=True,
        )

        # Create context menu
        self.create_menu(TermViewMenus.Context)

        # Create remote terminals menu
        self.remote_menu = self.create_menu(
            TerminalMainWidgetMenus.Remote,
            title=_("New terminal in remote server"),
        )

        # Add actions to options menu
        for item in [
            new_terminal_cwd,
            self.new_terminal_project,
            new_terminal_file,
            self.remote_menu,
        ]:
            self.add_item_to_menu(
                item, menu=menu, section=TerminalMainWidgetMenuSections.New
            )

        self.add_item_to_menu(
            rename_tab_action,
            menu=menu,
            section=TerminalMainWidgetMenuSections.TabActions,
        )

    def setup_remote_terminals_menu(self):
        self.remote_menu.clear_actions()

        for config_id in self._plugin._remote_client.get_config_ids():
            client_type = self.get_conf(
                option=f"{config_id}/auth_method", section="remoteclient"
            )
            name = self._plugin._remote_client.get_server_name(config_id)

            if client_type not in [
                AuthenticationMethod.Password,
                AuthenticationMethod.KeyFile,
            ]:
                continue

            action = self.create_action(
                name=config_id,
                text=f"New terminal in {name} server",
                triggered=functools.partial(
                    self.create_new_term,
                    config_id=config_id,
                ),
                overwrite=True,
            )
            self.add_item_to_menu(action, menu=self.remote_menu)

    def update_actions(self):
        """Setup and update the actions in the options menu."""
        if self.project_path is None:
            self.new_terminal_project.setEnabled(False)

    # ------ Private API ------------------------------------------
    def copy(self):
        if self.get_focus_widget():
            self.get_focus_widget().copy()

    def paste(self):
        if self.get_focus_widget():
            self.get_focus_widget().paste()

    def clear(self):
        if self.get_focus_widget():
            self.get_focus_widget().clear()

    def increase_font(self):
        if self.get_focus_widget():
            self.get_focus_widget().increase_font()

    def decrease_font(self):
        if self.get_focus_widget():
            self.get_focus_widget().decrease_font()

    def __wait_server_to_start(self):
        try:
            code = requests.get(
                "http://127.0.0.1:{0}".format(self.port)
            ).status_code
        except:
            code = 500

        if self.server_retries == self.MAX_SERVER_CONTACT_RETRIES:
            QMessageBox.critical(
                self,
                _("Spyder Terminal Error"),
                _(
                    "Terminal server could not be located at "
                    '<a href="http://127.0.0.1:{0}">'
                    "http://127.0.0.1:{0}</a>,"
                    " please restart Spyder on debugging mode "
                    "and open an issue with the contents of "
                    "<tt>{1}</tt> and <tt>{2}</tt> "
                    "files at {3}."
                ).format(
                    self.port,
                    self.stdout_file,
                    self.stderr_file,
                    self.URL_ISSUES,
                ),
                QMessageBox.Ok,
            )
        elif code != 200:
            self.server_retries += 1
            QTimer.singleShot(250, self.__wait_server_to_start)
        elif code == 200:
            self.sig_server_is_ready.emit()
            self.server_ready = True
            self.create_new_term(give_focus=False)

    # ------ Plugin API --------------------------------
    def update_font(self, font):
        """Update font from Preferences."""
        self.font = font
        for term in self.terms:
            term.set_font(font.family())

    def on_close(self, cancelable=False):
        """Perform actions before parent main window is closed."""
        self.closing = True
        for term in self.terms:
            term.close()
        self.server.kill()
        self.server.waitForFinished()
        return True

    def refresh_plugin(self):
        """Refresh tabwidget."""
        term = None
        if self.tabwidget.count():
            term = self.tabwidget.currentWidget()
            term.view.setFocus()
        else:
            term = None

    @on_conf_change
    def apply_plugin_settings(self, options):
        """Apply the config settings."""
        term_options = {}
        for option in options:
            if option == "color_scheme_name":
                term_options[option] = option
            else:
                term_options[option] = self.get_conf(option)
        for term in self.get_terms():
            term.apply_settings(term_options)

    # ------ Public API (for terminals) -------------------------
    def get_terms(self):
        """Return terminal list."""
        return [cl for cl in self.terms if isinstance(cl, TerminalWidget)]

    def get_current_term(self):
        """Return the currently selected terminal."""
        try:
            terminal = self.tabwidget.currentWidget()
        except AttributeError:
            terminal = None
        if terminal is not None:
            return terminal

    def reload_current_term(self):
        """Reload currently selected terminal."""
        current_term = self.get_current_term()
        if current_term:
            current_term.reload()

    def create_new_term(
        self, name=None, give_focus=True, path=None, config_id=None
    ):
        """Add a new terminal tab."""
        if path is None:
            path = self.current_cwd
        if self.project_path is not None:
            path = self.project_path
        path = path.replace("\\", "/")
        term = TerminalWidget(
            self,
            self.port,
            path=path,
            font=self.font.family(),
            theme=self.theme,
            color_scheme=self.color_scheme,
            config_id=config_id,
        )
        self.add_tab(term)
        term.terminal_closed.connect(lambda: self.close_term(term=term))

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
        if term:
            term.close()
        self.tabwidget.removeTab(self.tabwidget.indexOf(term))
        if term in self.terms:
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

    def server_is_ready(self):
        """Return server status."""
        return self.server_ready

    def search_next(self, text, case=False, regex=False, word=False):
        """Search in the current terminal for the given regex."""
        term = self.get_current_term()
        if term:
            term.search_next(text, case=case, regex=regex, word=word)

    def search_previous(self, text, case=False, regex=False, word=False):
        """Search in the current terminal for the given regex."""
        term = self.get_current_term()
        if term:
            term.search_previous(text, case=case, regex=regex, word=word)

    # ------ Public API (for tabs) ---------------------------
    def add_tab(self, widget):
        """Add tab."""
        self.terms.append(widget)
        num_term = self.tabwidget.count() + 1
        index = self.tabwidget.addTab(widget, "Terminal {0}".format(num_term))
        self.tabwidget.setCurrentIndex(index)
        self.tabwidget.setTabToolTip(index, "Terminal {0}".format(num_term))
        self.activateWindow()
        widget.view.setFocus()

    def move_tab(self, index_from, index_to):
        """
        Move tab (tabs themselves have already been moved by the tabwidget).

        Allows to change order of tabs.
        """
        term = self.terms.pop(index_from)
        self.terms.insert(index_to, term)

    def tab_name_editor(self):
        """Trigger the tab name editor."""
        index = self.tabwidget.currentIndex()
        self.tabwidget.tabBar().tab_name_editor.edit_tab(index)

    def handle_process_errors(self):
        """Handle when an error ocurrs in the server."""
        if not self.closing:
            QMessageBox.warning(
                self,
                _("Spyder Terminal Server Error"),
                _(
                    "The server that creates terminals failed to start. Please "
                    "restart Spyder in a system terminal with the command <tt> "
                    "spyder --debug-info minimal</tt> and open an issue with "
                    "the contents of <tt>{0}</tt> and <tt>{1}</tt> files at {2}."
                ).format(
                    osp.join(os.getcwd(), "spyder_terminal_out.log"),
                    osp.join(os.getcwd(), "spyder_terminal_err.log"),
                    self.URL_ISSUES,
                ),
                QMessageBox.Ok,
            )


def test():
    """Plugin visual test."""
    from spyder.utils.qthelpers import qapplication
    from unittest.mock import MagicMock

    app = qapplication(test_time=8)
    plugin_mock = MagicMock()
    term = TerminalMainWidget("terminal", plugin_mock, None)
    term.resize(900, 700)
    term._setup()
    term.setup()
    term.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test()
