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

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
coloredlogs.install(level='info')

clr = 'clear'
if os.name == 'nt':
    clr = 'cls'


def main(port):
    """Create and setup a new tornado server."""
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    settings = {"static_path": os.path.join(
        os.path.dirname(__file__), "static")}
    application = tornado.web.Application(routes.ROUTES,
                                          debug=True,
                                          serve_traceback=True,
                                          autoreload=True, **settings)
    print("Server is now at: 127.0.0.1:{}".format(port))
    application.term_manager = term_manager.TermManager()
    application.logger = LOGGER
    ioloop = tornado.ioloop.IOLoop.instance()
    application.listen(port, address='127.0.0.1')
    try:
        ioloop.start()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing server...\n")
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    os.system(clr)
    args = parser.parse_args()
    port = int(args.port)
    main(port)
