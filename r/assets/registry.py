import flask.ext.assets
import webassets.filter
import webassets.exceptions
import os
import subprocess
import tempfile
from r import app

_assets = flask.ext.assets.Environment(app)

class TSFilter(webassets.filter.Filter):
    name = 'ts'

    def setup(self):
        self.source_paths = []

    def input(self, _in, out, **kwargs):
        self.source_paths.append(kwargs.get('source_path'))

    def output(self, _in, out, **kwargs):
        output_filename = tempfile.mktemp() + '.js'
        args = ['tsc', '--out', output_filename] + self.source_paths
        proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=(os.name == 'nt')
        )

        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            raise webassets.exceptions.FilterError("typescript: subprocess had error: %s" % stdout)

        with open(output_filename, 'r') as f:
            out.write(f.read())

        os.unlink(output_filename)

webassets.filter.register_filter(TSFilter)

def _register(name, files, output, filters=None):
    _assets.register(name, flask.ext.assets.Bundle(*files, output='build/' + output, filters=filters))

def register_js(name, files, output):
    _register('js/' + name, ['js/' + file for file in files], 'js/' + output, 'jsmin')

def register_minified_js(name, files, output):
    _register('js/' + name, ['js/' + file for file in files], 'js/' + output)

def register_ts(name, files, output):
    _register('js/' + name, ['js/' + file for file in files], 'js/' + output, 'ts')
