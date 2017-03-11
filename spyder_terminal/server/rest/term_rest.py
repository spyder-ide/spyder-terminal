# -*- coding: iso-8859-15 -*-

import tornado.web
import tornado.escape


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self):
        self.status_code(403)

    @tornado.gen.coroutine
    def post(self):
        rows = int(self.get_argument('rows', None, 23))
        cols = int(self.get_argument('cols', None, 73))
        pid = yield self.application.term_manager.create_term(rows, cols)
        self.write(pid)


class ResizeHandler(tornado.web.RequestHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self):
        self.status_code(403)

    @tornado.gen.coroutine
    def post(self, pid):
        rows = int(self.get_argument('rows', None, 23))
        cols = int(self.get_argument('cols', None, 73))
        self.application.term_manager.resize_term(pid, rows, cols)
