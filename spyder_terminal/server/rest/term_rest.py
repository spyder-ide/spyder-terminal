# -*- coding: iso-8859-15 -*-

"""Main HTTP routes request handlers."""

import tornado.web
import tornado.escape
from os import getcwd


class MainHandler(tornado.web.RequestHandler):
    """Handles creation of new terminals."""

    @tornado.gen.coroutine
    def post(self):
        """POST verb: Create a new terminal."""
        rows = int(self.get_argument('rows', None, 23))
        cols = int(self.get_argument('cols', None, 73))
        cwd = self.get_cookie('cwd', default=getcwd())
        self.application.logger.info('CWD: {0}'.format(cwd))
        pid = yield self.application.term_manager.create_term(rows, cols, cwd)
        self.write(pid)


class ResizeHandler(tornado.web.RequestHandler):
    """Handles resizing of terminals."""

    @tornado.gen.coroutine
    def post(self, pid):
        """POST verb: Resize a terminal."""
        rows = int(self.get_argument('rows', None, 23))
        cols = int(self.get_argument('cols', None, 73))
        self.application.term_manager.resize_term(pid, rows, cols)
