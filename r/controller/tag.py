from flask import request
import r.model.tag
from r import app

@app.route('/tags/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('q', '')
    tags = r.model.tag.with_prefix(prefix)
    return r.lib.success_response({'tags': tags})
