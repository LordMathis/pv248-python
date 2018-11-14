from sys import argv
import pandas as pd
import numpy as np
import json

def read_data(fname):
    return pd.read_csv(fname)

def proc_dates(data):
    pass

def proc_deadlines(data):

    result = {}

    for column in data.columns.values:

        if column == 'student':
            continue

        mean = data[column].mean()
        quartiles = data[column].quantile([0.25,0.5,0.75])
        passed = data[column].astype(bool).sum()

        result[column] = {
            'mean': mean,
            'median': quartiles[0.5],
            'first': quartiles[0.25],
            'last': quartiles[0.75],
            'passed': passed
        }

    return result


def proc_exercises(data):
    pass

'''https://stackoverflow.com/a/50577730'''
def default(o):
    if isinstance(o, np.int64): return int(o)
    raise TypeError

def print_json(data):
    print(json.dumps(data,
                     indent=4,
                     sort_keys=False,
                     ensure_ascii=False,
                     default=default))

if __name__ == '__main__':

    fname = argv[1]
    mode = argv[2]

    data = read_data(fname)

    if mode == 'dates':
        proc_dates(data)
    elif mode == 'deadlines':
        res = proc_deadlines(data)
        print_json(res)
    elif mode == 'exercises':
        proc_exercises(data)
    else:
        print('Unknown mode')
