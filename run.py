import datetime
import os
import subprocess

import click
import pandas as pd

import command as c
import dicom

OUTPUT_DIR = 'data'


def _get_file_name(year, month, day, mod):
    file_name = os.path.join(OUTPUT_DIR, 'data-')
    if year:
        return file_name + year + '.csv'
    if month:
        return file_name + month + '.csv'
    else:
        return file_name + day + '-' + mod + '.csv'


def _execute(cmds):
    frames = []
    cmd_len = len(cmds)
    for i, cmd in enumerate(cmds, start=1):
        click.echo('Running cmd ' + str(i) + ' of ' + str(cmd_len))
        completed = subprocess.run(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        lines = completed.stderr.decode('latin1').splitlines()
        frames.append(pd.DataFrame.from_dict(dicom.get_headers(lines)))

    result_df = pd.concat(frames)
    return result_df


def _write_file(df, file_name):
    df.to_csv(file_name, header=True, index=False, sep=';')


def _debug_file(debug, cmds):
    with open(debug, 'w') as command_file:
        for cmd in cmds:
            command_file.write(' '.join(cmd))
            command_file.write('\n')


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
    cmds = []
    year_cmds = []

    if year:
        query_year = datetime.datetime.strptime(year, '%Y')
        year_cmds = c.create_full_year_cmds(query_year)

    if month:
        year_month = datetime.datetime.strptime(month, '%Y-%m')
        cmds = c.create_year_month_cmds(year_month)
    else:
        query_date = datetime.datetime.strptime(day, '%Y-%m-%d')
        cmds = c.create_cmds(query_date, mod)

    if debug:
        click.echo('Running debug mode, commands are written to %s', debug)
        _debug_file(debug, cmds)
    else:
        click.echo('Running query mode')
        if year:
            for month in year_cmds:
                click.echo('Running month %s', month)
                result_df = _execute(month)
                file_name = _get_file_name(year, month, day, mod)
                _write_file(result_df, file_name)
                click.echo('Month %s finised', month)
        else:
            result_df = _execute(cmds)
            file_name = _get_file_name(year, month, day, mod)
            _write_file(result_df, file_name)
