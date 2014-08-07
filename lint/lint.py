import argparse
import os
import subprocess
import sys

RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
DEFAULT = "\033[39m"

to_print = {"E": RED, "W": YELLOW, "C": YELLOW, "F": YELLOW}


# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--include-warnings', dest="include_warnings", action='store_true', help='include warnings/cautions')
args = parser.parse_args()

path = os.path.dirname(os.path.realpath(__file__))
rcfile = path + '/pylint-rc'

py_files = []
for root, dirs, files in os.walk(os.path.dirname(path)):
    for file in files:
        if file.endswith(".py"):
            py_files.append(os.path.join(root, file))
py_files.sort()

error_string = "" if args.include_warnings else " --errors-only "
p = subprocess.Popen('pylint --reports=n --rcfile=%s %s %s' % (rcfile, error_string, " ".join(py_files)), shell=True, stdout=subprocess.PIPE)
out, err = p.communicate()

file_line = ""
printed = False
for line in out.splitlines():
    # python3 sends bytestrings
    line = line.decode('utf-8')
    if line[0] == '*':
        file_line = line
        printed = False
    elif line[0] in to_print:
        if not printed:
            printed = True
            print(file_line)
        print(to_print[line[0]]+line+DEFAULT)
