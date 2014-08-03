from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import review.db

app = Flask(__name__)

app.secret_key = "this needs to change"

import review.controller.user

