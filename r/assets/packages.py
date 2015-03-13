import os
import r.assets.packager
from r import app

packager = r.assets.packager.Packager(
    os.path.dirname(r.__file__) + '/',
    app.static_folder + '/build/'
)

def register():
    packager.register('js/lib.min.js', [
        packager.asset.minified_javascript('static/src/js/lib/jquery-1.11.1.min.js'),
        packager.asset.minified_javascript('static/src/js/lib/underscore-min.js'),
        packager.asset.minified_javascript('static/src/js/lib/nunjucks.min.js')
    ])

    packager.register('js/review.min.js', [
        packager.asset.typescript('static/src/js/pages/review.ts')
    ])

    packager.register('js/upload.min.js', [
        packager.asset.typescript('static/src/js/pages/upload.ts')
    ])

def build():
    packager.build_packages()
