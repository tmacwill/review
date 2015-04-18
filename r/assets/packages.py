import os
import r
from r import app

packager = None

def css():
    return {
        'css/lib.min.css': [
            packager.asset.css('static/src/css/lib/bootstrap.min.css'),
            packager.asset.css('static/src/css/global.css')
        ],

        'css/browse.min.css': [
            packager.asset.css('static/src/css/macros/typeahead.css'),
            packager.asset.css('static/src/css/pages/browse.css')
        ],

        'css/error.min.css': [
            packager.asset.css('static/src/css/pages/error.css')
        ],

        'css/login.min.css': [
            packager.asset.css('static/src/css/macros/login_box.css'),
            packager.asset.css('static/src/css/pages/login.css')
        ],

        'css/notifications.min.css': [
            packager.asset.css('static/src/css/pages/notifications.css')
        ],

        'css/profile.min.css': [
            packager.asset.css('static/src/css/pages/profile.css')
        ],

        'css/review.min.css': [
            packager.asset.css('static/src/css/macros/login_box.css'),
            packager.asset.css('static/src/css/pages/review.css')
        ],

        'css/upload.min.css': [
            packager.asset.css('static/src/css/macros/typeahead.css'),
            packager.asset.css('static/src/css/pages/upload.css')
        ]
    }

def js():
    return {
        'js/lib.min.js': [
            packager.asset.minified_javascript('static/src/js/lib/jquery-1.11.1.min.js'),
            packager.asset.minified_javascript('static/src/js/lib/underscore-min.js'),
            packager.asset.minified_javascript('static/src/js/lib/nunjucks.min.js'),
            packager.asset.minified_javascript('static/src/js/lib/moment.min.js'),
            packager.asset.minified_javascript('static/src/js/lib/events.min.js')
        ],

        'js/browse.min.js': [
            packager.asset.typescript('static/src/js/pages/browse.ts')
        ],

        'js/profile.min.js':  [
            packager.asset.typescript('static/src/js/pages/profile.ts')
        ],

        'js/review.min.js': [
            packager.asset.typescript('static/src/js/pages/review.ts'),
            packager.asset.template('templates/macros/comment_box.html')
        ],

        'js/upload.min.js': [
            packager.asset.typescript('static/src/js/pages/upload.ts')
        ]
    }

def register():
    global packager
    packager = r.assets.packager.Packager(
        os.path.dirname(r.__file__) + '/',
        app.static_folder + '/build/'
    )

    packager.register_multi(css())
    packager.register_multi(js())

def build_packages():
    packager.build_packages()

def build_package(package_name):
    packager.build_package(package_name)

def monitor():
    packager.monitor()
