# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import tornado.escape
import tornado.websocket


class MainSocket(tornado.websocket.WebSocketHandler):
    def open(self, pid, *args, **kwargs):
        # self.application.pc.add_event_listener(self)
        print("WebSocket opened")
        print(pid)
        self.pid = pid
        self.application.term_manager.start_term(pid, self)
        print("TTY On!")

    def on_close(self):
        print("WebSocket closed")
        self.application.term_manager.stop_term(self.pid)
        # self.application.pc.remove_event_listener(self)

    def on_message(self, message):
        # print(message)
        self.application.term_manager.execute(self.pid, message)
        #"op_type;amount;acc_local;acc_remote"
        # print message

    def notify(self, message):
        # print(message)
        self.write_message(message)