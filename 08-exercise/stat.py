from sys import argv
import pandas as pd
import utils

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

if __name__ == '__main__':

    fname = argv[1]
    mode = argv[2]

    data = utils.read_data(fname)
    dates_dframe, ex_dframe = utils.make_dframes(data)

    if mode == 'dates':
        utils.print_json(proc_data(dates_dframe))
    elif mode == 'deadlines':
        utils.print_json(proc_data(data))
    elif mode == 'exercises':
        utils.print_json(proc_data(ex_dframe))
    else:
        print('Unknown mode')
