import os
import logging
import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext

logging.warning(os.getcwd())
DATABASE = 'flaskr/SERP-database/serp.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@click.command('init-db')
@with_appcontext
def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

# @current_app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


