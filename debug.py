import sys
from r import app

host = '0.0.0.0'
if len(sys.argv) > 1:
    host = sys.argv[1]

port = 8080
if len(sys.argv) > 2:
    port = int(sys.argv[2])

import r.assets.packages
r.assets.packages.register()
r.assets.packages.build()

app.run(debug=True, host=host, port=port)
