from sys import argv
import pandas as pd
import numpy as np
import json
import utils

if __name__ == '__main__':

    fname = argv[1]
    id = argv[2]

    data = utils.read_data(fname)
    print(data)
