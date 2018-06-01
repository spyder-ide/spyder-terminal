# -*- coding: iso-8859-15 -*-

"""
routes.

======

This module establishes and defines the Web Handlers and Websockets
that are associated with a specific URL routing name. New routing
associations must be defined here.

Notes
-----
For more information regarding routing URL and valid regular expressions
visit: http://www.tornadoweb.org/en/stable/guide/structure.html
"""

import spyder_terminal.server.web as web
import spyder_terminal.server.rest as rest
import spyder_terminal.server.websockets as websockets

# Define new rest associations
REST = [
    (r"/api/terminals", rest.term_rest.MainHandler),
    (r"/api/terminals/(.*)/size", rest.term_rest.ResizeHandler)
]

# Define new websocket routes
WS = [
    (r"/terminals/(.*)", websockets.term_ws.MainSocket)
]

# Define new web rendering route associations
WEB = [
    (r'/', web.main_handler.MainHandler)
]

ROUTES = REST + WS + WEB
