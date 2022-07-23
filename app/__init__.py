"""Init file for app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as SQL

def create_app(config = None):
    db = SQL()
    app = Flask(__name__)
    return app