# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Terminal Plugin."""

# Standard imports
from functools import cached_property
import os
import os.path as osp

# Third party imports
from qtpy.QtCore import Signal
from spyder.api.fonts import SpyderFontType
from spyder.api.plugins import Plugins, SpyderDockablePlugin
from spyder.api.plugin_registration.decorators import (
    on_plugin_available,
    on_plugin_teardown,
)
from spyder.config.base import get_translation

# Local imports
from spyder_terminal.confpage import TerminalConfigPage
from spyder_terminal.config import CONF_DEFAULTS, CONF_VERSION
from spyder_terminal.widgets.main_widget import TerminalMainWidget

# Constants
LOCATION = osp.realpath(osp.join(os.getcwd(),
                                 osp.dirname(__file__)))
WINDOWS = os.name == 'nt'

# For translations
_ = get_translation('spyder_terminal')


class TerminalPlugin(SpyderDockablePlugin):
    """
    Terminal plugin.
    """
    NAME = 'terminal'
    REQUIRES = [Plugins.Preferences]
    OPTIONAL = [
        Plugins.Projects,
        Plugins.Editor,
        Plugins.WorkingDirectory,
        Plugins.RemoteClient,
    ]
    TABIFY = [Plugins.IPythonConsole]
    CONF_SECTION = NAME
    WIDGET_CLASS = TerminalMainWidget
    CONF_FILE = True
    CONF_WIDGET_CLASS = TerminalConfigPage
    CONF_DEFAULTS = CONF_DEFAULTS
    CONF_VERSION = CONF_VERSION
    CAN_BE_DISABLED = False

    # --- Signals
    # ------------------------------------------------------------------------
    sig_server_is_ready = Signal()
    """
    This signal is emitted when the server is ready to connect.
    """

    # ---- SpyderDockablePlugin API
    # ------------------------------------------------------------------------
    @staticmethod
    def get_name():
        """Return plugin title."""
        return _('Terminal')

    def get_description(self):
        """Return the description of the explorer widget."""
        return _("Create system terminals inside Spyder.")

    def get_icon(self):
        """Return widget icon."""
        return self.create_icon('DollarFileIcon')

    def on_initialize(self):
        """Initialize the plugin."""
        self.update_font()
        self.get_widget().sig_server_is_ready.connect(self.sig_server_is_ready)

    @on_plugin_available(plugin=Plugins.WorkingDirectory)
    def on_working_directory_available(self):
        """Connect when working directory is available."""
        workingdirectory = self.get_plugin(Plugins.WorkingDirectory)
        workingdirectory.sig_current_directory_changed.connect(
            self.set_current_cwd)

    @on_plugin_available(plugin=Plugins.Projects)
    def on_projects_available(self):
        """Connect when projects is available."""
        projects = self.get_plugin(Plugins.Projects)
        projects.sig_project_loaded.connect(self.set_project_path)
        projects.sig_project_closed.connect(self.unset_project_path)

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_available(self):
        """Connect when editor available."""
        editor = self.get_plugin(Plugins.Editor)
        editor.sig_file_opened_closed_or_updated.connect(
            self.set_current_opened_file)

    @on_plugin_available(plugin=Plugins.Preferences)
    def on_preferences_available(self):
        """Connect when preferences available."""
        preferences = self.get_plugin(Plugins.Preferences)
        preferences.register_plugin_preferences(self)

    @on_plugin_available(plugin=Plugins.RemoteClient)
    def on_remoteclient_available(self):
        """Connect when preferences available."""
        remoteclient = self.get_plugin(Plugins.RemoteClient)
        widget = self.get_widget()

        remoteclient.sig_server_changed.connect(
            widget.setup_remote_terminals_menu
        )
        widget.setup_remote_terminals_menu()

    @on_plugin_teardown(plugin=Plugins.RemoteClient)
    def on_remoteclient_teardown(self):
        """Connect when preferences available."""
        remoteclient = self.get_plugin(Plugins.RemoteClient)
        widget = self.get_widget()

        remoteclient.sig_server_changed.disconnect(
            widget.setup_remote_terminals_menu
        )

    def update_font(self):
        """Update font from Preferences."""
        font = self.get_font(SpyderFontType.Monospace)
        self.get_widget().update_font(font)

    def check_compatibility(self):
        """Check if current Qt backend version is greater or equal to 5."""
        message = ''
        valid = True
        if WINDOWS:
            try:
                import winpty
                del winpty
            except:
                message = _('Unfortunately, the library that <b>spyder-termina'
                            'l</b> uses to create terminals is failing to '
                            'work in your system. Therefore, this plugin will '
                            'be deactivated.<br><br> This usually happens on '
                            'Windows 7 systems. If that\'s the case, please '
                            'consider updating to a newer Windows version.')
                valid = False
        return valid, message

    def on_close(self, cancelable=False):
        """Perform actions before closing the plugin."""
        return self.get_widget().on_close(cancelable=False)

    def refresh(self):
        """Refresh main widget."""
        self.get_widget().refresh()

    def set_current_cwd(self, cwd):
        """Set the current working directory to the new one."""
        self.get_widget().set_current_cwd(cwd)

    def set_project_path(self, path):
        self.get_widget().set_project_path(path)

    def unset_project_path(self, _path):
        self.get_widget().unset_project_path()

    def set_current_opened_file(self, filename, _language):
        self.get_widget().set_current_opened_file(filename)

    def create_new_term(self, **kwargs):
        self.get_widget().create_new_term(**kwargs)

    @cached_property
    def _remote_client(self):
        return self.get_plugin(Plugins.RemoteClient)
