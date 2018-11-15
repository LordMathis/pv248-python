from sys import argv
import pandas as pd
import numpy as np
import utils

def get_student_data(id, data):
    print(data.loc[id, : ])

if __name__ == '__main__':

    fname = argv[1]
    id = argv[2]

    data = utils.read_data(fname)
    dates_dframe, ex_dframe = utils.make_dframes(data)

    if id == 'average':
        pass
    else:
        id = int(id)
        get_student_data(id, data)
