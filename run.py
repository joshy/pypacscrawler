import click
import datetime
import logging
from logging.config import fileConfig

import pypacscrawler.command as c
import pypacscrawler.writer as w
from pypacscrawler.query import query_day, query_month, query_year


@click.command()
@click.option('--year', help='Year to query for, if year is set other options \
                              are ignored. For each month a separate file is \
                              created')
@click.option('--month', help='Month of year to query, format is yyyy-mm')
@click.option('--day', help='Day to query for, format is yyyy-mm-dd')
@click.option('--mod', help='Modality to query for')
def cli(year, month, day, mod):
    """ This script queries the pacs and generates a json file. """
    fileConfig('logging.ini')
    logger = logging.getLogger()
    if not year and not month and not day:
        click.echo('No year, month or day was given')
        exit(1)

    if year:
        logging.info('Runnig year %s', year)
        results = query_year(year)
        w.write_results(results, month, day, mod)
    elif month:
        logging.info('Running month %s', month)
        results = query_month(month)
        w.write_results(results, month, day, mod)
    else:
        logging.info('Running day %s', day)
        logging.info('Running mod %s', )
        query_date = datetime.datetime.strptime(day, '%Y-%m-%d')
        results = query_day(mod, query_date, c.INITIAL_TIME_RANGE)
        w.write_results(results, month, day, mod)


if __name__ == '__main__':
    cli()
