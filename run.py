import datetime
import click


import pypacscrawler.command as c
from pypacscrawler import writer
from pypacscrawler.query import query_day, query_month, query_year


@click.command()
@click.option('--year', help='Year to query for, if year is set other options \
                              are ignored. For each month a separate file is \
                              created')
@click.option('--month', help='Month of year to query, format is yyyy-mm')
@click.option('--day', help='Day to query for, format is yyyy-mm-dd')
@click.option('--mod', help='Modality to query for')
def cli(year, month, day, mod,):
    """ This script queries the pacs and generates a csv file. """
    if not year and not month and not day:
        click.echo('No year, month or day was given')
        exit(1)

    if year:
        query_year(year)
    elif month:
        query_month(month)
    else:
        query_date = datetime.datetime.strptime(day, '%Y-%m-%d')
        results = query_day(mod, query_date, c.INITIAL_TIME_RANGE)
        file_name = writer.get_file_name(month, day, mod)
        writer.write_results(results, file_name)


if __name__ == '__main__':
    cli()
