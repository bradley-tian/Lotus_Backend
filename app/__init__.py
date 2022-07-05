"""Init file for app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as SQL
from flask_cors import CORS

db = SQL()
app = Flask(__name__)
cors = CORS(app)

from app import views