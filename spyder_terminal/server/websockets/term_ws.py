# -*- coding: iso-8859-15 -*-

import tornado.escape
import tornado.websocket


class MainSocket(tornado.websocket.WebSocketHandler):
    def open(self, pid, *args, **kwargs):
        print("WebSocket opened")
        print(pid)
        self.pid = pid
        self.application.term_manager.start_term(pid, self)
        print("TTY On!")

    def on_close(self):
        print('TTY Off!')
        print("WebSocket closed")
        self.application.term_manager.stop_term(self.pid)

    def on_message(self, message):
        self.application.term_manager.execute(self.pid, message)

    def notify(self, message):
        self.write_message(message)
