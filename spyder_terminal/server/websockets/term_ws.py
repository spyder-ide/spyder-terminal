# -*- coding: iso-8859-15 -*-

"""Websocket handling class."""

import tornado.escape
import tornado.websocket


class MainSocket(tornado.websocket.WebSocketHandler):
    """Handles long polling communication between xterm.js and server."""

    def open(self, pid, *args, **kwargs):
        """Opens a Websocket associated to a console."""
        print("WebSocket opened")
        print(pid)
        self.pid = pid
        self.application.term_manager.start_term(pid, self)
        print("TTY On!")

    def on_close(self):
        """Closes console communication."""
        print('TTY Off!')
        print("WebSocket closed")
        self.application.term_manager.stop_term(self.pid)

    def on_message(self, message):
        """Executes a command on console."""
        self.application.term_manager.execute(self.pid, message)

    def notify(self, message):
        """Writes stdout/err to client."""
        self.write_message(message)
