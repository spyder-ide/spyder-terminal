
"""General server constants and utillty functions."""

import tornado
import os.path
import spyder_terminal.server.routes as routes
from spyder_terminal.server.logic.term_manager import TermManager

# These shell options ensure proper startup in "interactive login" mode
SHOPTS = {
    'bash': ['-i', '-l'],
    'zsh': ['-i', '-l'],
    'fish': ['-i', '-l'],
    'sh': ['-i', '-l'],
    'ksh': ['-i', '-l'],
    'csh': ['-i', '-l'],
    'pwsh': [],
    'rbash': ['-i', '-l'],
    'dash': ['-i', '-l'],
    'screen': ['-l'],
    'tmux': [],
    'tcsh': ['-i', '-l'],
    'xonsh': [],
    'cmd': []
}


def create_app(shell, close_future=None):
    """Create and return a tornado Web Application instance."""
    settings = {"static_path": os.path.join(
        os.path.dirname(__file__), "static")}
    application = tornado.web.Application(routes.gen_routes(close_future),
                                          debug=True,
                                          serve_traceback=True,
                                          autoreload=True, **settings)
    shell_base = os.path.basename(shell).split('.')[0]
    application.term_manager = TermManager([shell] + SHOPTS[shell_base])
    return application
