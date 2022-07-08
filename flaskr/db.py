import os
import logging
import sqlite3

from flask import current_app, g

logging.warning(os.getcwd())
DATABASE = 'flaskr/SERP-database/serp.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db



# @current_app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


