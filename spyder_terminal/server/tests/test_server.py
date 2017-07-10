
"""
Tornado server-side tests.

Note: This uses tornado.testing unittest style tests
"""

import os
import sys
import os.path as osp
sys.path.append(osp.realpath(osp.dirname(__file__) + "/.."))

from spyder.utils.programs import find_program
from main import create_app
from tornado import testing, httpserver, gen, websocket


SHELL = '/usr/bin/env bash'
WINDOWS = os.name == 'nt'

if WINDOWS:
    SHELL = find_program('cmd.exe')


class TerminalServerTests(testing.AsyncHTTPTestCase):
    """Main server tests."""
    def get_app(self):
        return create_app(SHELL)

    def _mk_connection(self):
        return websocket.websocket_connect(
            'ws://localhost:{}/'.format(self.port)
        )

    @testing.gen_test
    def test_main_get(self):
        response = yield self.http_client.fetch(
            self.get_url('/'),
            method="GET"
        )
        self.assertEqual(response.code, 200)

    @testing.gen_test
    def test_main_post(self):
        try:
            yield self.http_client.fetch(
                self.get_url('/'),
                method="POST",
                body=''
            )
        except Exception:
            pass
        # self.assertEqual(response.code, 403)
