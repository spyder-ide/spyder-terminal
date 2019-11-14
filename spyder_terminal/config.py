import os

WINDOWS = os.name == 'nt'

CONF_DEFAULTS = [('terminal',
                 {
                  'sound': True,
                  'cursor_style': 'bar',
                  'shell': 'cmd' if WINDOWS else 'bash'
                  }),
                 ]

CONF_VERSION = '1.0.0'
