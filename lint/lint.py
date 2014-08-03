import os

path = os.path.dirname(os.path.realpath(__file__))
rcfile = path + '/pylint-rc'

os.chdir(os.path.dirname(path))
os.system('find . -name "*.py" | xargs pylint --reports=n --rcfile=%s' % (rcfile))
