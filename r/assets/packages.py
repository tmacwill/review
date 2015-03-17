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
        packager.asset.minified_javascript('static/src/js/lib/nunjucks.min.js'),
        packager.asset.minified_javascript('static/src/js/lib/moment.min.js')
    ])

    packager.register('js/review.min.js', [
        packager.asset.typescript('static/src/js/pages/review.ts'),
        packager.asset.template('templates/macros/comment_box.html')
    ])

    packager.register('js/upload.min.js', [
        packager.asset.typescript('static/src/js/pages/upload.ts')
    ])

def build_packages():
    packager.build_packages()

def build_package(package_name):
    packager.build_package(package_name)

def monitor():
    packager.monitor()
