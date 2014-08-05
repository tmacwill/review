import os
import subprocess

RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
DEFAULT = "\033[39m"

to_print = {"E": RED, "W": YELLOW, "C": YELLOW, "F": YELLOW}
path = os.path.dirname(os.path.realpath(__file__))
rcfile = path + '/pylint-rc'

py_files = []
for root, dirs, files in os.walk(os.path.dirname(path)):
    for file in files:
        if file.endswith(".py"):
            py_files.append(os.path.join(root, file))
py_files.sort()

p = subprocess.Popen('pylint --reports=n --rcfile=%s %s' % (rcfile, " ".join(py_files)), shell=True, stdout=subprocess.PIPE)
out, err = p.communicate()
file_line = ""
printed = False
for line in out.splitlines():
    if line[0] == '*':
        file_line = line
        printed = False
    elif line[0] in to_print:
        if not printed:
            printed = True
            print file_line
        print to_print[line[0]],line,DEFAULT
