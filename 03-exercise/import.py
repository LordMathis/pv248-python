from sys import argv
import utils

if __name__ == '__main__':
    input = argv[1]
    output = argv[2]

    print(utils.load(input))
