# -*- coding: iso-8859-15 -*-

import tornado.web
import tornado.escape


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, db=None):
        self.db = db

    @tornado.gen.coroutine
    def get(self):
        self.render('../static/index.html')

    @tornado.gen.coroutine
    def post(self):
        self.set_status(403)
