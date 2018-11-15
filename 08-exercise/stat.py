from sys import argv
import pandas as pd
import numpy as np
import json

def read_data(fname):
    return pd.read_csv(fname)

def make_dframes(data):
    dates_dframe = pd.DataFrame()
    ex_dframe = pd.DataFrame()

    for column in data.columns.values:

        if column == 'student':
            dates_dframe['student'] = data['student']
            ex_dframe['student'] = data['student']
            continue

        column_split = column.split('/')

        if column_split[0] in dates_dframe.columns:
            dates_dframe[column_split[0]] += data[column]
        else:
            dates_dframe[column_split[0]] = data[column]

        if column_split[1] in ex_dframe.columns:
            ex_dframe[column_split[1]] += data[column]
        else:
            ex_dframe[column_split[1]] = data[column]


    return dates_dframe, ex_dframe

def proc_data(data):

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
    dates_dframe, ex_dframe = make_dframes(data)

    if mode == 'dates':
        print_json(proc_data(dates_dframe))
    elif mode == 'deadlines':
        print_json(proc_data(data))
    elif mode == 'exercises':
        print_json(proc_data(ex_dframe))
    else:
        print('Unknown mode')
