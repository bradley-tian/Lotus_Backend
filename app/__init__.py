"""Init file for app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as SQL

db = SQL()
app = Flask(__name__)