from sys import argv
from numpy import linalg

if __name__ == '__main__':

    input = argv[1]
    content = ''

    with open(input, 'r') as ins:
        content = ins.read()

    print(content)
