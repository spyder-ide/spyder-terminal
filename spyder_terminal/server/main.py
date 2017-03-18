#!/usr/bin/env python

import os
import routes
import logging
import coloredlogs
import tornado.web
import tornado.ioloop
from logic import term_manager


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
coloredlogs.install(level='info')

clr = 'clear'
if os.name == 'nt':
    clr = 'cls'


def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    settings = {"static_path": os.path.join(
        os.path.dirname(__file__), "static")}
    application = tornado.web.Application(routes.ROUTES,
                                          debug=True,
                                          serve_traceback=True,
                                          autoreload=True, **settings)
    print("Server is now at: 127.0.0.1:8000")
    application.term_manager = term_manager.TermManager()
    application.logger = LOGGER
    ioloop = tornado.ioloop.IOLoop.instance()
    application.listen(8000, address='127.0.0.1')
    try:
        ioloop.start()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing server...\n")
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    os.system(clr)
    main()
