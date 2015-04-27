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
def build_package(package_name):
    """ Build a single package. """

    import r.assets.packages
    r.assets.packages.register()
    r.assets.packages.build_package(package_name)

@manager.command
def build_packages():
    """ Build all static packages. """

    import r.assets.packages
    r.assets.packages.register()
    r.assets.packages.build_packages()

@manager.command
def monitor_packages():
    """ Monitor static files for changes. """

    import r.assets.packages
    build_packages()
    r.assets.packages.monitor(block=True)

@manager.command
def reset():
    """ Reset the schema. """

    import r

    path = os.path.dirname(os.path.realpath(__file__)) + '/r/schema'
    migrations_path = path + '/migrations/'
    data_path = path + '/data/'

    # start with a fresh database
    os.system("mysql -uroot -e 'drop database review' >/dev/null 2>&1")
    os.system("mysql -uroot -e 'create database review'")

    # run all migrations in order
    migrations = [i for i in sorted(os.listdir(migrations_path), key=lambda e: int(e.split('.')[0]))]
    for file in migrations:
        os.system("mysql -uroot review < " + migrations_path + file)

    # populate data
    data = os.listdir(data_path)
    for file in data:
        os.system("mysql -uroot review < " + data_path + file)

    r.store._flush_I_KNOW_WHAT_IM_DOING()
    sync_store()

@flask_failsafe.failsafe
@manager.command
@manager.option('-h', '--host', help='Host')
@manager.option('-p', '--port', help='Port')
def runserver(host='0.0.0.0', port='9000'):
    """ Run the development server and monitor changes to assets. """

    # enable debug mode
    os.environ['DEBUG'] = '1'

    # flask doesn't reload nested macros, so manually add them all to the watch list
    extra_directories = [os.path.dirname(os.path.realpath(__file__)) + '/r/templates/macros/']
    extra_files = []
    for extra_directory in extra_directories:
        for directory, directories, files in os.walk(extra_directory):
            for filename in files:
                filename = os.path.join(directory, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)

    # only start the package monitor the first time we're run
    if not os.environ.get('REVIEW_SERVER_RUNNING'):
        import r.assets.packages
        r.assets.packages.register()
        r.assets.packages.build_packages()
        r.assets.packages.monitor()

    os.environ['REVIEW_SERVER_RUNNING'] = '1'
    manager.app.run(debug=True, host=host, port=int(port), extra_files=extra_files)

@manager.command
def sync_store():
    """ Sync data from the database to the store. """

    import r
    r.model.tag.sync_to_store()

if __name__ == "__main__":
    manager.run()
