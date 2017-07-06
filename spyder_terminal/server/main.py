#!/usr/bin/env python

"""Main terminal server point of entry."""

import argparse
import logging
import os
import routes

import coloredlogs
import tornado.web
import tornado.ioloop

from logic import term_manager


parser = argparse.ArgumentParser(
    description='Websocket-based bash terminal server')

parser.add_argument('--port',
                    default=8070,
                    help="TCP port to be listened on")
parser.add_argument('--shell',
                    default='/usr/bin/env bash',
                    help="name/path to the terminal process to execute")

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
coloredlogs.install(level='info')

clr = 'clear'
if os.name == 'nt':
    clr = 'cls'


def main(port, shell):
    """Create and setup a new tornado server."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    settings = {"static_path": os.path.join(
        os.path.dirname(__file__), "static")}
    application = tornado.web.Application(routes.ROUTES,
                                          debug=True,
                                          serve_traceback=True,
                                          autoreload=True, **settings)
    LOGGER.info("Server is now at: 127.0.0.1:{}".format(port))
    LOGGER.info('Shell: {0}'.format(shell))
    application.term_manager = term_manager.TermManager(shell)
    application.logger = LOGGER
    ioloop = tornado.ioloop.IOLoop.instance()
    application.listen(port, address='127.0.0.1')
    try:
        ioloop.start()
    except KeyboardInterrupt:
        pass
    finally:
        LOGGER.info("Closing server...\n")
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    args = parser.parse_args()
    port = int(args.port)
    shell = args.shell
    main(port, shell)
