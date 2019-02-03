import sys

def read_file(path):
    with open(path) as input:
        return input.read()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def report(file, line, desc):
    eprint('{}:{}: {}'.format(file, line, desc))