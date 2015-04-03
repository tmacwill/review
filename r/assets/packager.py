import os
import subprocess
import tempfile
import collections
import watchdog.observers
import watchdog.events
import time
import re

class BuildError(Exception):
    pass

Asset = collections.namedtuple('Asset', [
    'asset_type',
    'path'
])

Package = collections.namedtuple('Package', [
    'package_name',
    'assets'
])

class FileChangedEventHandler(watchdog.events.FileSystemEventHandler):
    def set_packager(self, packager):
        self.packager = packager

    def on_modified(self, event):
        self.packager.on_modified(event.src_path)

class Packager(object):
    def __init__(self, source, build, debug=True):
        self.source = source
        self.build = build
        self.debug = debug
        self.packages = {}
        self.dependencies = {}
        self.last_modified = {}
        self.asset = AssetFactory(self.source)
        self.builders = {
            'minified_javascript': MinifiedJavascriptBuilder(),
            'template': TemplateBuilder(),
            'typescript': TypeScriptBuilder()
        }

    def _build_asset(self, asset):
        if not asset.asset_type in self.builders:
            print("Unknown asset type: %s" % asset.asset_type)

        # map the asset type to a builder and write output to a temporary file
        output = tempfile.mktemp()
        builder = self.builders[asset.asset_type]
        builder.build(asset, output)
        return output

    def _concatenate(self, files: list, output: str):
        # make sure directory to output file exists
        os.system('mkdir -p ' + os.path.dirname(output))

        # cat all files into the output file, overwriting it
        args = ['cat'] + files + ['>', output]
        os.system(' '.join(args))

    def _is_modified(self, path):
        return self.last_modified.get(path, 0) != os.path.getmtime(path)

    def _register_dependency(self, package, asset):
        self.dependencies.setdefault(asset.path, [])
        self.dependencies[asset.path].append(package)

    def _register_dependencies(self, package, asset):
        self._register_dependency(package, asset)

        # extract references/imports from the file
        with open(asset.path, 'r') as f:
            contents = f.read()
            references = re.findall(r'/// <reference path="([^"]+)" />', contents)

            # recursively add all references
            for reference in references:
                path = os.path.normpath(os.path.dirname(asset.path) + '/' + reference + os.path.splitext(asset.path)[1])
                self._register_dependencies(package, self.asset._asset(asset_type=asset.asset_type, path=path))

    def _set_modified(self, path):
        self.last_modified[path] = os.path.getmtime(path)

    def build_packages(self):
        """ Build all registered packages. """

        for package in self.packages.keys():
            self.build_package(package)

    def build_package(self, package_name: str):
        """ Build a single package. """

        if self.debug:
            print('Started building', package_name)

        # build each asset, then concatenate all output into a single package
        package = self.packages[package_name]
        output = [self._build_asset(asset) for asset in package.assets]
        self._concatenate(output, self.build + package.package_name)

        # delete temporary files
        for path in output:
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass

        if self.debug:
            print('Finished building', package_name)

    def monitor(self, block=False):
        """ Monitor the current directory for changes. """

        # start a watchdog monitor on the source directory
        event_handler = FileChangedEventHandler()
        event_handler.set_packager(self)
        self.observer = watchdog.observers.Observer()
        self.observer.schedule(event_handler, path=self.source, recursive=True)
        self.observer.start()

        if not block:
            return self.observer

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def on_modified(self, path: str):
        """ Called whenever a file we're monitoring is modified. """

        if not path in self.dependencies or not self._is_modified(path):
            return

        # when a file is modified, get all the packages that depend on it and build them
        self._set_modified(path)
        packages = self.dependencies.get(path, [])
        for package in packages:
            self.build_package(package.package_name)

    def register(self, package_name: str, assets: list):
        """ Register a new package. """

        package = Package(package_name=package_name, assets=assets)

        # register dependencies
        for asset in assets:
            self._register_dependencies(package, asset)

        self.packages[package_name] = package
        return package

class AssetFactory(object):
    def __init__(self, source):
        self.source = source

    def _asset(self, asset_type, path):
        return Asset(asset_type=asset_type, path=path)

    def minified_javascript(self, path):
        return self._asset(asset_type='minified_javascript', path=self.source + path)

    def template(self, path):
        return self._asset(asset_type='template', path=self.source + path)

    def typescript(self, path):
        return self._asset(asset_type='typescript', path=self.source + path)

class _Builder(object):
    def run(self, args, capture=True):
        if capture:
            # run the given command, reading in stdout and stderr so we can output if there's an error
            process = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=(os.name == 'nt')
            )

            stdout, stderr = process.communicate()
            if process.returncode != 0:
                print("Packaging error!\n%s" % stdout.decode('utf-8'))

        else:
            os.system(' '.join(args))

    def build(self, asset, output):
        raise NotImplementedError()

class MinifiedJavascriptBuilder(_Builder):
    def build(self, asset, output):
        self.run(['cat', asset.path, '>', output], capture=False)

class TemplateBuilder(_Builder):
    def build(self, asset, output):
        # each template contains macro and endmacro tags, so strip those before precompiling
        with open(asset.path, 'r') as read:
            tmp = tempfile.mktemp()
            with open(tmp, 'w') as write:
                write.writelines(read.readlines()[1:-1])

            self.run(['nunjucks-precompile', '--name', os.path.basename(asset.path), tmp, '>', output], capture=False)
            os.unlink(tmp)

class TypeScriptBuilder(_Builder):
    def build(self, asset, output):
        self.run(['tsc', '--out', output, asset.path])
