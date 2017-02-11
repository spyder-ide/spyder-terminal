# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import tornado.web
import tornado.escape
# import logic.tm as tm

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self):
        self.status_code(403)

    @tornado.gen.coroutine
    def post(self):
        pid = yield self.application.term_manager.create_term()
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
        # self.status_code(403)
        # self.write(pid)