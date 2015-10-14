from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "SECRET"
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models