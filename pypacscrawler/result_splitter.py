# Finds out the time ranges for a given day

from pypacscrawler.command import basic_query, add_time, add_day, add_modality
from pypacscrawler.time_splitter import split
from pypacscrawler.executor import run


def query_day(mod, day, time_range):
    print('-----------------------')
    print(time_range)
    print('-----------------------')
    query = prepare_query(mod, day, time_range)
    result, size = run(query)

    if size < 500:
        print('result < 500 for {}'.format(time_range))
        return [result]
    else:
        print('results >= 500 for {}, splitting'.format(time_range))
        l, r = split(time_range)
        return [query_day(mod, day, l),
                query_day(mod, day, r)]


def prepare_query(mod, day, time_range):
    query = add_day(basic_query(), day)
    query = add_modality(query, mod)
    query = add_time(query, time_range)
    return query
