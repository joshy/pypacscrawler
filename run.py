import datetime
import os
import subprocess

import click
import pandas as pd

import command as c
import dicom

OUTPUT_DIR = 'data'

def get_file_name(year, month, day, mod):
    file_name = os.path.join(OUTPUT_DIR, 'data-')
    if year:
        return file_name + year + '.csv'
    if month:
        return file_name + month + '.csv'
    else:
        return file_name + day + '-' + mod + '.csv'


@click.command()
@click.option('--year', help='Year to query for, if year is set other options \
                              are ignored (except --file)')
@click.option('--month', help='Month of year to year, format is yyyy-mm')
@click.option('--date', help='Date to query for, format is yyyy-mm-dd')
@click.option('--mod', help='Modality to query for')
@click.option('--debug', help='Print out commands to passed file name, \
                               doesn\'t query the PACS')
def cli(year, month, day, mod, debug):
    """ This script queries the pacs and generates a csv file. """
    cmds = []

    if year:
        query_year = datetime.datetime.strptime(year, '%Y')
        cmds = c.create_full_year_cmds(query_year)
    if month:
        year_month = datetime.datetime.strptime(month, '%Y-%m')
        cmds = c.create_year_month_cmds(year_month)
    else:
        query_date = datetime.datetime.strptime(day, '%Y-%m-%d')
        cmds = c.create_cmds(query_date, mod)

    if debug:
        click.echo('Running debug mode')
        with open(debug, 'w') as command_file:
            for cmd in cmds:
                command_file.write(' '.join(cmd))
                command_file.write('\n')
    else:
        click.echo('Running query mode')
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
        file_name = get_file_name(year, month, day, mod)
        result_df.to_csv(file_name, header=True, index=False)
