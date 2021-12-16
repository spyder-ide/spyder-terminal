# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Spyder Terminal Plugin."""

from .terminalplugin import TerminalPlugin as PLUGIN_CLASS

PLUGIN_CLASS

VERSION_INFO = (1, 2, 0)
__version__ = '.'.join(map(str, VERSION_INFO))
