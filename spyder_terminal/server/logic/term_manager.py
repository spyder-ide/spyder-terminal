# -*- coding: utf-8 -*-

"""Term manager."""

from __future__ import unicode_literals

import os
import time
import hashlib
import tornado.web
import tornado.gen
import tornado.ioloop

WINDOWS = 'nt'

if os.name == WINDOWS:
    import winpty as pty
else:
    import pexpect as pty


class TermReader(object):
    """This class allows to read continously from a terminal stream."""

    def __init__(self, tty, socket):
        """Terminal reader constructor."""
        self.tty = tty
        self.socket = socket
        self.p_callback = tornado.ioloop.PeriodicCallback(self.consume_lines,
                                                          callback_time=10)
        self.p_callback.start()

    @tornado.gen.coroutine
    def consume_lines(self):
        """Consume lines from stream each 100ms."""
        try:
            timeout = 0
            if os.name == WINDOWS:
                _in = self.tty.read(1000)
                self.socket.notify(_in)
            else:
                if self.tty.isalive():
                    _in = self.tty.read_nonblocking(timeout=timeout, size=1000)
                    self.socket.notify(_in)
                else:
                    self.socket.close()
        except Exception:
            pass


class TermManager(object):
    """Wrapper around pexpect to execute local commands."""

    def __init__(self):
        """Main terminal handler constructor."""
        self.os = os.name
        if self.os == WINDOWS:
            self.cmd = r'C:\windows\system32\cmd.exe'
        else:
            self.cmd = '/usr/bin/env bash'
        self.sockets = {}
        self.consoles = {}

    @tornado.gen.coroutine
    def create_term(self, rows, cols):
        """Create a new virtual terminal."""
        pid = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[0:6]
        if self.os == WINDOWS:
            tty = pty.PTY(cols, rows)
            tty.spawn(self.cmd)
        else:
            tty = pty.spawnu(self.cmd)
            tty.setwinsize(rows, cols)
        self.consoles[pid] = {'tty': tty, 'read': None}
        raise tornado.gen.Return(pid)

    @tornado.gen.coroutine
    def start_term(self, pid, socket):
        """Start reading a virtual terminal."""
        term = self.consoles[pid]
        self.sockets[pid] = socket
        if self.os != WINDOWS:
            term['tty'].expect('')
        term['read'] = TermReader(term['tty'], socket)

    @tornado.gen.coroutine
    def stop_term(self, pid):
        """Stop and close terminal."""
        term = self.consoles[pid]
        term['tty'].close()
        del self.consoles[pid]
        del self.sockets[pid]

    @tornado.gen.coroutine
    def execute(self, pid, cmd):
        """Write characters to terminal."""
        term = self.consoles[pid]['tty']
        if self.os == WINDOWS:
            term.write(cmd)
        else:
            term.send(cmd)

    @tornado.gen.coroutine
    def resize_term(self, pid, rows, cols):
        """Resize terminal."""
        term = self.consoles[pid]['tty']
        if self.os != WINDOWS:
            term.setwinsize(rows, cols)
        else:
            term.set_size(cols, rows)
