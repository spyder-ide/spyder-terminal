# -*- coding: iso-8859-15 -*-

import os
import sys
import json
import datetime
import tornado.web
import tornado.escape
import db.dbconn as db
import dao.utils as utils
import dao.users_dao as users
import dao.flights_dao as flights
import dao.countries_dao as countries


@tornado.gen.coroutine
def list_countries(iso_code):
    conn = db.get_instance()
    if iso_code is None:
       results = yield conn.run_transaction(countries.get_countries)
    else:
       results = yield conn.run_transaction(countries.get_country, iso_code)
    raise tornado.gen.Return(results)

@tornado.gen.coroutine
def list_flights(data, col_name, start, length, order):
    conn = db.get_instance()
    total_size = 506190
    # total_size = total_size[0]['total']
    if data is None:
       results = yield conn.run_transaction(flights.get_flights, col_name, start, length, order)
       filtered = total_size
    else:
       results, filtered = yield conn.run_transaction(flights.get_flights_from_to_date, data, col_name, start, length, order)

    # total_records = yield conn.run_transaction(flights.get_total_num)
    raise tornado.gen.Return((results, total_size,filtered))

@tornado.gen.coroutine
def register_user(user):
    conn = db.get_instance()
    result = yield conn.run_transaction(users.register_user, user)
    raise tornado.gen.Return(result)

