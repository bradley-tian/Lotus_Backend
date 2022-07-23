"""Init file for app."""
from flask import Flask
from importlib import import_module
from flask_sqlalchemy import SQLAlchemy as SQL

db = SQL()

def register_blueprints(app):
    module = import_module("app.base.views".format('base'))
    app.register_blueprint(module.blueprint)

def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.init_app(app=app)
        db.create_all(app=app)

def create_app(config = None):
    app = Flask(__name__, template_folder = "/base/templates", static_folder = "/base/static")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    register_blueprints(app)
    configure_database(app)
    return app