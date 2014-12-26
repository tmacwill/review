from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

# this is just a development key. production will use a key not checked into the repo.
app.secret_key = b'R\xdaF[f\xed\xc9\xd5\x81P\xec\xdb4G\xb8\xc6\xecj%\x13\x00\x1a\x08c'

import review.bundle

import review.controller.comment
import review.controller.upload
import review.controller.user
