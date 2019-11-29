import os

WINDOWS = os.name == 'nt'

CONF_DEFAULTS = [('terminal',
                 {
                  'sound': True,
                  'cursor_type': 0,
                  'shell': 'cmd' if WINDOWS else 'bash'
                  }),
                 ]

CONF_VERSION = '1.0.0'
