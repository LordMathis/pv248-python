from sys import argv
import pandas as pd
import numpy as np
import utils
import math
from scipy.optimize import curve_fit
from datetime import datetime, timedelta

format = "%Y-%m-%d"

def get_student_data(id, data):
    return data.loc[id, : ]

def date_to_day(date, start_day='2018-09-17'):
    start = datetime.strptime(start_day, format)
    curr = datetime.strptime(date, format)

    return (curr - start).days

def add_days(days, start_day='2018-09-17'):
    start = datetime.strptime(start_day, format)
    return start + timedelta(days)

def date_to_string(date):
    return datetime.strftime(date, format)

def calc_avg(data):
    return data.mean(axis=0)

def process_student(stud_dates, stud_exs):

    cum_pts = stud_dates.cumsum()
    cum_pts = cum_pts.rename(lambda x: date_to_day(x))

    x = cum_pts.index
    y = cum_pts.values

    slope = curve_fit(lambda x, y: x * y, x, y)[0][0]

    if slope == 0:
        date_16 = 'inf'
        date_20 = 'inf'
    else:
        day_16 = int(16 / slope)
        day_20 = int(20 / slope)

        date_16 = date_to_string(add_days(day_16))
        date_20 = date_to_string(add_days(day_20))

    res = {
        'mean': stud_exs.mean(),
        'median': stud_exs.median(),
        'total': stud_exs.sum(),
        'passed': stud_exs.astype(bool).sum(),
        'regression slope': slope,
        'date 16': date_16,
        'date 20': date_20
    }

    return res

if __name__ == '__main__':

    fname = argv[1]
    id = argv[2]

    data = utils.read_data(fname)

    if id == 'average':
        avg_data = calc_avg(data)
        date_avg = pd.Series()
        ex_avg = pd.Series()

        for i, v in avg_data.items():

            i_splt = i.split('/')

            if i_splt[0] in date_avg:
                date_avg[i_splt[0]] += v
            else:
                date_avg[i_splt[0]] = v

            if i_splt[1] in ex_avg:
                ex_avg[i_splt[1]] += v
            else:
                ex_avg[i_splt[1]] = v

        res = process_student(date_avg, ex_avg)
        utils.print_json(res)

    else:
        id = int(id)

        dates_dframe, ex_dframe = utils.make_dframes(data)

        stud_exs = get_student_data(id, ex_dframe)
        stud_dates = get_student_data(id, dates_dframe)

        res = process_student(stud_dates, stud_exs)
        utils.print_json(res)
