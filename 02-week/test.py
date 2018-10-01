from sys import argv
import scorelib

if __name__ == '__main__':
    filename = argv[1]
    prints = scorelib.load(filename)
    for p in prints:
        p.format()
        print()
