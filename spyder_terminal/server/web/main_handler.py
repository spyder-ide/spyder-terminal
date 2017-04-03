# -*- coding: iso-8859-15 -*-

import tornado.web
import tornado.escape


class MainHandler(tornado.web.RequestHandler):
    """Handles index request."""

    def initialize(self, db=None):
        """Stump initialization function."""
        self.db = db

    @tornado.gen.coroutine
    def get(self):
        """Get static index.html page."""
        self.render('../static/index.html')

    @tornado.gen.coroutine
    def post(self):
        """POST verb: Forbidden."""
        self.set_status(403)
