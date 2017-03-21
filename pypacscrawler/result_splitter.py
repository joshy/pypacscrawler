# Finds out the time ranges for a given day

from pypacscrawler.command import scout_query, add_time, add_day, add_modality
from pypacscrawler.time_splitter import split
from pypacscrawler.executor import run


def time_ranges_per_day(mod, day, time_range):
    query = prepare_query(mod, day, time_range)
    print('running query')
    result, size = run(query)

    if size < 500:
        print('result < 500 for {}'.format(time_range))
        return [time_range]
    else:
        print('results >= 500 for {}, splitting'.format(time_range))
        l, r = split(time_range)
        l_q = prepare_query(day, l)
        r_q = prepare_query(day, r)
        return [time_ranges_per_day(day, l_q), time_ranges_per_day(day, r_q)]


def prepare_query(mod, day, time_range):
    query = add_day(scout_query(), day)
    query = add_modality(query, mod)
    query = add_time(query, time_range)
    return query
