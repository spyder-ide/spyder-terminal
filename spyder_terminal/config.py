# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""Spyder terminal default configuration."""

import os
import sys

WINDOWS = os.name == 'nt'
LINUX = sys.platform.startswith('linux')

CONF_SECTION = 'terminal'

CONF_DEFAULTS = [
    (CONF_SECTION,
     {
      'sound': True,
      'cursor_type': 0,
      'shell': 'cmd' if WINDOWS else 'bash',
      'buffer_limit': 1000
     }
     ),
    ('shortcuts',
     {
      'terminal/copy': 'Ctrl+Alt+Shift+C' if LINUX else 'Ctrl+Alt+C',
      'terminal/paste': 'Ctrl+Alt+Shift+V' if LINUX else 'Ctrl+Alt+V',
      'terminal/new terminal': 'Ctrl+Alt+T',
      'terminal/clear': 'Ctrl+Alt+K',
      'terminal/zoom in': 'Ctrl++',
      'terminal/zoom out': 'Ctrl+-',
     }
     ),
]

# IMPORTANT NOTES:
# 1. If you want to *change* the default value of a current option, you need to
#    do a MINOR update in config version, e.g. from 1.0.0 to 1.1.0
# 2. If you want to *remove* options that are no longer needed in our codebase,
#    or if you want to *rename* options, then you need to do a MAJOR update in
#    version, e.g. from 1.0.0 to 2.0.0
# 3. You don't need to touch this value if you're just adding a new option
CONF_VERSION = '2.0.0'
