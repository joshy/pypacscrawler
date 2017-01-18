import datetime
import os
import subprocess

import click
import pandas as pd

import command as c
import dicom
import writer


def _execute(cmds):
    frames = []
    with click.progressbar(cmds,
                           label='Running commands') as commands:
        for cmd in commands:
            completed = subprocess.run(cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            lines = completed.stderr.decode('latin1').splitlines()
            frames.append(pd.DataFrame.from_dict(dicom.get_headers(lines)))

    result_df = pd.concat(frames)
    return result_df


@click.command()
@click.option('--year', help='Year to query for, if year is set other options \
                              are ignored (except --debug). For each month \
                              a separate file is created')
@click.option('--month', help='Month of year to query, format is yyyy-mm')
@click.option('--day', help='Day to query for, format is yyyy-mm-dd')
@click.option('--mod', help='Modality to query for')
@click.option('--debug', help='Print out commands to passed file name, \
                               doesn\'t query the PACS')
def cli(year, month, day, mod, debug):
    """ This script queries the pacs and generates a csv file. """
    if not year and not month and not day:
        click.echo('No input was given')
        exit(1)

    cmds = []
    year_cmds = []

    if year:
        query_year = datetime.datetime.strptime(year, '%Y')
        click.echo('Start: Generating commands for year ' + year)
        year_cmds = c.create_full_year_cmds(query_year)
        click.echo('End: Generating commands for year ' + year)
    elif month:
        year_month = datetime.datetime.strptime(month, '%Y-%m')
        cmds = c.create_year_month_cmds(year_month)
    else:
        query_date = datetime.datetime.strptime(day, '%Y-%m-%d')
        cmds = c.create_cmds(query_date, mod)

    if debug:
        click.echo('Running debug mode, commands are written to %s', debug)
        writer.debug_file(debug, cmds)
    else:
        click.echo('Running query mode')
        if year:
            for i, month in enumerate(year_cmds, start=1):
                click.echo('Start: Running month ' + str(i))
                result_df = _execute(month)
                file_name = writer.get_file_name(month, day, mod)
                writer.write_file(result_df, file_name)
                click.echo('End: Running month ' + str(i))
        else:
            result_df = _execute(cmds)
            file_name = writer.get_file_name(month, day, mod)
            writer.write_file(result_df, file_name)
