
"""General server constants and utillty functions."""

import tornado
import os.path
import spyder_terminal.server.routes as routes
from spyder_terminal.server.logic.term_manager import TermManager


def create_app(shell, close_future=None):
    """Create and return a tornado Web Application instance."""
    settings = {"static_path": os.path.join(
        os.path.dirname(__file__), "static")}
    application = tornado.web.Application(routes.ROUTES,
                                          debug=True,
                                          serve_traceback=True,
                                          autoreload=True, **settings)
    application.term_manager = TermManager([shell])
    return application
