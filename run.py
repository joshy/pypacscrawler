import subprocess
import datetime

import pandas as pd
import click

import dicom
import command as c


@click.command()
@click.option('--year', help='Year to query for')
@click.option('--date', help='Specific date to query for, format is yyyy-mm-dd')
@click.option('--mod', help='Specific modality to query for')
@click.option('--dry', default=False, help='Just print out command, don\'t query')
def cli(year, date, mod, dry):
    """ This script queries the pacs and generates a csv file. """
    cmds = []
    if year:
        cmds = c.create_full_year_cmds()
    else:
        query_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        cmds = c.create_cmds(query_date, mod)

    if dry:
        click.echo('Running dry mode')
        with open('commands.txt', 'w') as command_file:
            for cmd in cmds:
                command_file.write(' '.join(cmd))
                command_file.write('\n')
    else:
        click.echo('Running query mode')
        df = pd.DataFrame()
        cmd_len = len(cmds)
        for i, cmd in enumerate(cmds, start=1):
            click.echo('Running cmd ' + str(i) + ' of ' + str(cmd_len))
            completed = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            lines = completed.stderr.decode('latin1').splitlines()
            df.append(dicom.get_headers(lines))

        df.to_csv("data.csv", header=True, index=False)
