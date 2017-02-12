# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Terminal Plugin."""

from spyder.api.plugins import SpyderPluginWidget

from spyder.api.preferences import PluginConfigPage



class TerminalConfigPage(PluginConfigPage):
    """Terminal plugin preferences."""
    pass


class TerminalPlugin(SpyderPluginWidget):
    """Terminal plugin."""
    pass


