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
    
    logging.warning(os.getcwd())
    DATABASE = 'flaskr/SERP-database/serp.db'

    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @app.route('/testdb')
    def testdb():
        crsr = get_db().cursor()
        # execute the command to fetch all the data from the table emp
        crsr.execute("SELECT * FROM organic")
        
        # store all the fetched data in the ans variable
        ans = crsr.fetchall()
        logging.warning(ans)
        return '<h1>It works.</h1>'

    




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

    return app