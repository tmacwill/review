import flask.ext.script
import flask_failsafe
import sys
import os

@flask_failsafe.failsafe
def create_app():
    from r import app
    return app

manager = flask.ext.script.Manager(create_app())

@manager.command
def build_packages():
    """ Build all static packages. """

    import r.assets.packages
    r.assets.packages.register()
    r.assets.packages.build()

@manager.command
def monitor_packages():
    """ Monitor static files for changes. """

    import r.assets.packages
    build_packages()
    r.assets.packages.monitor(block=True)

@flask_failsafe.failsafe
@manager.command
@manager.option('-h', '--host', help='Host')
@manager.option('-p', '--port', help='Port')
def runserver(host='0.0.0.0', port=9000):
    """ Run the development server and monitor changes to assets. """

    # only start the package monitor the first time we're run
    if not os.environ.get('REVIEW_SERVER_RUNNING'):
        import r.assets.packages
        r.assets.packages.register()
        r.assets.packages.build()
        r.assets.packages.monitor()

    os.environ['REVIEW_SERVER_RUNNING'] = '1'
    manager.app.run(debug=True, host=host, port=port)

if __name__ == "__main__":
    manager.run()
