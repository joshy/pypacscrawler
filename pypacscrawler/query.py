# Finds out the time ranges for a given day
import sys
import datetime as datetime
import pandas as pd

from typing import List, Dict
from pypacscrawler.command import basic_query, add_time, add_day, \
    add_modality, year_start_end, MODALITIES, INITIAL_TIME_RANGE
from pypacscrawler.time import split
from pypacscrawler.executor import run


def query_year(year):
    # type: (str) -> List[Dict[str, str]]
    start, end = year_start_end(year)
    # MS is month start frequency
    months = pd.date_range(start, end, freq='MS')
    results = []
    for month in months:
        results.extend(query_month(month.strftime('%Y-%m')))
    return results


def query_month(year_month):
    # type: (str) -> List[Dict[str, str]]
    print('\nRunning month: {}'.format(year_month))
    start = datetime.datetime.strptime(year_month, '%Y-%m')
    end = start + pd.tseries.offsets.MonthEnd()
    results = []
    for day in pd.date_range(start, end):
        for mod in MODALITIES:
            results.extend(query_day(mod, day, INITIAL_TIME_RANGE))
    return results


def query_day(mod, day, time_range):
    # type: (str, str, str) -> List[Dict[str, str]]
    query = prepare_query(mod, day, time_range)
    result, size = run(query)

    if size < 500:
        sys.stdout.write('.')
        sys.stdout.flush()
        return [result]
    else:
        print('results >= 500 for {} {} {}, splitting'
              .format(mod, day, time_range))
        l, r = split(time_range)
        return query_day(mod, day, l) + query_day(mod, day, r)


def prepare_query(mod, day, time_range):
    query = add_day(basic_query(), day)
    query = add_modality(query, mod)
    query = add_time(query, time_range)
    return query
