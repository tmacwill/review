from flask import Flask

app = Flask(__name__)

# this is just a development key. production will use a key not checked into the repo.
app.secret_key = b'R\xdaF[f\xed\xc9\xd5\x81P\xec\xdb4G\xb8\xc6\xecj%\x13\x00\x1a\x08c'

import r.assets
import r.store
import r.db
import r.lib

r.store.configure()

import r.controller
import r.model

import r.test
