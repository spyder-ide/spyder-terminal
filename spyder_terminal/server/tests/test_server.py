
"""
Tornado server-side tests.

Note: This uses tornado.testing unittest style tests
"""

import os
import sys
import os.path as osp

PY3 = sys.version_info[0] == 3

if PY3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode

import pytest
from flaky import flaky
from tornado import testing, websocket, gen
from tornado.concurrent import Future
from spyder.utils.programs import find_program

sys.path.append(osp.realpath(osp.dirname(__file__) + "/.."))

from main import create_app

LOCATION = os.path.realpath(os.path.join(os.getcwd(),
                                         os.path.dirname(__file__)))
LOCATION_SLASH = LOCATION.replace('\\', '/')

LINE_END = '\n'
SHELL = '/usr/bin/env bash'
WINDOWS = os.name == 'nt'

if WINDOWS:
    LINE_END = '\r\n'
    SHELL = find_program('cmd.exe')


class TerminalServerTests(testing.AsyncHTTPTestCase):
    """Main server tests."""

    def get_app(self):
        """Return HTTP/WS server."""
        self.close_future = Future()
        return create_app(SHELL, self.close_future)

    def _mk_connection(self, pid):
        return websocket.websocket_connect(
            'ws://127.0.0.1:{0}/terminals/{1}'.format(
                self.get_http_port(), pid)
        )

    @gen.coroutine
    def close(self, ws):
        """
        Close a websocket connection and wait for the server side.

        If we don't wait here, there are sometimes leak warnings in the
        tests.
        """
        ws.close()
        yield self.close_future

    @testing.gen_test
    def test_main_get(self):
        """Test if HTML source is rendered."""
        response = yield self.http_client.fetch(
            self.get_url('/'),
            method="GET"
        )
        self.assertEqual(response.code, 200)

    @testing.gen_test
    def test_main_post(self):
        """Test that POST requests to root are forbidden."""
        try:
            yield self.http_client.fetch(
                self.get_url('/'),
                method="POST",
                body=''
            )
        except Exception:
            pass

    @testing.gen_test
    def test_create_terminal(self):
        """Test terminal creation."""
        data = {'rows': '25', 'cols': '80'}
        response = yield self.http_client.fetch(
            self.get_url('/api/terminals'),
            method="POST",
            body=urlencode(data)
        )
        self.assertEqual(response.code, 200)

    @flaky(max_runs=3)
    @testing.gen_test
    def test_terminal_communication(self):
        """Test terminal creation."""
        data = {'rows': '25', 'cols': '100'}
        response = yield self.http_client.fetch(
            self.get_url('/api/terminals'),
            method="POST",
            body=urlencode(data)
        )
        pid = response.body.decode('utf-8')
        sock = yield self._mk_connection(pid)
        msg = yield sock.read_message()
        print(msg)
        test_msg = 'pwd'
        sock.write_message(' ' + test_msg)
        msg = ''
        while test_msg not in msg:
            msg = yield sock.read_message()
            print(msg)
        self.assertTrue(test_msg in msg)

    # @pytest.mark.skipif(os.name == 'nt', reason="It doesn't work on Windows")
    @testing.gen_test
    def test_terminal_closing(self):
        """Test terminal destruction."""
        data = {'rows': '25', 'cols': '80'}
        response = yield self.http_client.fetch(
            self.get_url('/api/terminals'),
            method="POST",
            body=urlencode(data)
        )
        pid = response.body.decode('utf-8')
        sock = yield self._mk_connection(pid)
        _ = yield sock.read_message()
        yield self.close(sock)
        try:
            sock.write_message(' This shall not work')
        except AttributeError:
            pass

    @flaky(max_runs=3)
    @testing.gen_test
    def test_terminal_resize(self):
        """Test terminal resizing."""
        data = {'rows': '25', 'cols': '80'}
        response = yield self.http_client.fetch(
            self.get_url('/api/terminals'),
            method="POST",
            body=urlencode(data)
        )

        pid = response.body.decode('utf-8')
        sock = yield self._mk_connection(pid)
        _ = yield sock.read_message()

        data = {'rows': '23', 'cols': '73'}
        response = yield self.http_client.fetch(
            self.get_url('/api/terminals/{0}/size'.format(pid)),
            method="POST",
            body=urlencode(data)
        )

        sock.write_message('cd {0}{1}'.format(LOCATION_SLASH, LINE_END))

        python_exec = 'python print_size.py' + LINE_END
        sock.write_message(python_exec)

        expected_size = '(73, 23)'
        msg = ''
        while expected_size not in msg:
            msg = yield sock.read_message()
        self.assertIn(expected_size, msg)
