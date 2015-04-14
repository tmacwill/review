import os
import r
from r import app

packager = None

def register():
    global packager
    packager = r.assets.packager.Packager(
        os.path.dirname(r.__file__) + '/',
        app.static_folder + '/build/'
    )

    packager.register('css/lib.min.css', [
        packager.asset.css('static/src/css/lib/bootstrap.min.css'),
        packager.asset.css('static/src/css/global.css'),
    ])

    packager.register('css/browse.min.css', [
        packager.asset.css('static/src/css/macros/typeahead.css'),
        packager.asset.css('static/src/css/pages/browse.css'),
    ])

    packager.register('css/login.min.css', [
        packager.asset.css('static/src/css/pages/login.css'),
    ])

    packager.register('css/notifications.min.css', [
        packager.asset.css('static/src/css/pages/notifications.css'),
    ])

    packager.register('css/profile.min.css', [
        packager.asset.css('static/src/css/pages/profile.css'),
    ])

    packager.register('css/review.min.css', [
        packager.asset.css('static/src/css/pages/review.css'),
    ])

    packager.register('css/upload.min.css', [
        packager.asset.css('static/src/css/macros/typeahead.css'),
        packager.asset.css('static/src/css/pages/upload.css'),
    ])

    packager.register('js/lib.min.js', [
        packager.asset.minified_javascript('static/src/js/lib/jquery-1.11.1.min.js'),
        packager.asset.minified_javascript('static/src/js/lib/underscore-min.js'),
        packager.asset.minified_javascript('static/src/js/lib/nunjucks.min.js'),
        packager.asset.minified_javascript('static/src/js/lib/moment.min.js'),
        packager.asset.minified_javascript('static/src/js/lib/events.min.js'),
    ])

    packager.register('js/browse.min.js', [
        packager.asset.typescript('static/src/js/pages/browse.ts')
    ])

    packager.register('js/profile.min.js', [
        packager.asset.typescript('static/src/js/pages/profile.ts')
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
