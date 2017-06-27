# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Spyder Project Contributors
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""Spyder Terminal Plugin."""

from qtpy import PYQT5

if PYQT5:
    from .terminalplugin import TerminalPlugin as PLUGIN_CLASS

VERSION_INFO = (0, 2, 'dev0')
__version__ = '.'.join(map(str, VERSION_INFO))
