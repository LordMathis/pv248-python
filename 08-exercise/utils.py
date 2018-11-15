import pandas as pd
import numpy as np
import json

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

def read_data(fname):
    return pd.read_csv(fname)
