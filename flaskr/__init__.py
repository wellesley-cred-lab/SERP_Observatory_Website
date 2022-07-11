import os
import sqlite3
import logging

from flask import Flask, g
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text

# testing database connection
logging.warning(os.getcwd())


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import categories
    app.register_blueprint(categories.bp)
    app.add_url_rule('/', endpoint='index')

    from . import dates
    app.register_blueprint(dates.bp)

    from . import serps
    app.register_blueprint(serps.bp)

    from . import db
    #db.init_app(app)

    from . import rankchanges
    app.register_blueprint(rankchanges.bp)

    return app