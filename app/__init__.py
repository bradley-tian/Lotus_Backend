"""Init file for app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as SQL

db = SQL()

def create_app(config = None):
    app = Flask(__name__, template_folder='templates')
    return app