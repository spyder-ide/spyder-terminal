# -*- coding: utf-8 -*-

"""Term manager."""

from __future__ import unicode_literals

import os
import time
import pexpect
import hashlib
import tornado.web
import tornado.gen
import tornado.ioloop
import pexpect.popen_spawn as pspawn

WINDOWS = 'nt'


class TermReader(object):
    """This class allows to read continously from a terminal stream."""

    def __init__(self, tty, socket):
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
                timeout = 100
                self.tty.expect('')
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
        self.os = os.name
        if self.os == WINDOWS:
            self.cmd = 'cmd'
            self.pty_fork = lambda x: pspawn.PopenSpawn(x, encoding="utf-8")
        else:
            self.cmd = '/usr/bin/env bash'
            self.pty_fork = pexpect.spawnu
        self.sockets = {}
        self.consoles = {}

    @tornado.gen.coroutine
    def create_term(self, rows, cols):
        """Create a new virtual terminal."""
        pid = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()[0:6]
        tty = self.pty_fork(self.cmd)
        self.consoles[pid] = {'tty': tty, 'read': None}
        self.resize_term(pid, rows, cols)
        raise tornado.gen.Return(pid)

    @tornado.gen.coroutine
    def start_term(self, pid, socket):
        """Start reading a virtual terminal."""
        term = self.consoles[pid]
        self.sockets[pid] = socket
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
            self.sockets[pid].notify(cmd)
            print(repr(cmd))
            if cmd == '\n' or cmd == '\r\n' or cmd == '\r':
                term.sendline()
        term.send(cmd)

    @tornado.gen.coroutine
    def resize_term(self, pid, rows, cols):
        """Resize terminal."""
        if self.os != WINDOWS:
            term = self.consoles[pid]['tty']
            term.setwinsize(rows, cols)
