import r.assets.registry

def build():
    r.assets.registry.register_minified_js('lib', [
        'lib/jquery-1.11.1.min.js',
        'lib/underscore-min.js',
        'lib/nunjucks.min.js',
    ], 'lib.min.js')

    r.assets.registry.register_ts('review', [
        'review.ts'
    ], 'review.min.js')
