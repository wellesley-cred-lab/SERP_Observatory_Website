import os

from flask import Flask


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
    app.add_url_rule('/6-8-22', endpoint='date')

    return app