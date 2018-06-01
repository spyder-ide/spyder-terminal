# -*- coding: iso-8859-15 -*-

"""Websocket handling class."""

import logging
import tornado.escape
import tornado.websocket

LOGGER = logging.getLogger(__name__)

class MainSocket(tornado.websocket.WebSocketHandler):
    """Handles long polling communication between xterm.js and server."""

    def initialize(self, close_future=None):
        """Base class initialization."""
        self.close_future = close_future

    def open(self, pid):
        """Open a Websocket associated to a console."""
        LOGGER.info("WebSocket opened: {0}".format(pid))
        self.pid = pid
        self.application.term_manager.start_term(pid, self)
        LOGGER.info("TTY On!")

    def on_close(self):
        """Close console communication."""
        LOGGER.info('TTY Off!')
        LOGGER.info("WebSocket closed: {0}".format(self.pid))
        self.application.term_manager.stop_term(self.pid)
        if self.close_future is not None:
            self.close_future.set_result(("Done!"))

    def on_message(self, message):
        """Execute a command on console."""
        self.application.term_manager.execute(self.pid, message)

    def notify(self, message):
        """Write stdout/err to client."""
        self.write_message(message)
