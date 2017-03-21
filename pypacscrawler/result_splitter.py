# Finds out the time ranges for a given day

from pypacscrawler.command import scout_query, add_time, add_day
from pypacscrawler.time_splitter import split
from pypacscrawler.executor import run


def time_ranges_per_day(day, time_range):
    query = prepare_query(day, time_range)
    result, size = run(query, time_range)

    if size < 500:
        return [time_range]
    else:
        l, r = split(time_range)
        l_q = prepare_query(day, l)
        r_q = prepare_query(day, r)
        return [time_ranges_per_day(day, l_q), time_ranges_per_day(day, r_q)]


def prepare_query(day, time_range):
    query = add_day(scout_query(), day)
    query = add_time(query, time_range)
    return query
