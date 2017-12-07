import luigi
import pandas as pd
import requests
from urllib import parse
from pathlib import Path
import pypacscrawler.command as cmd
import pypacscrawler.executor as exec
from pypacscrawler.config import solr_settings
import pypacscrawler.writer as w
import time
import os

status_dir = 'data/status'
if not os.path.exists(status_dir):
    os.makedirs(status_dir)


def get_json_path(accession_number):
    file_path_no_ext = os.path.join(status_dir, accession_number)
    return '{}.json'.format(file_path_no_ext)


def get_solr_core_url():
    solr_core_url = solr_settings()['solr_core_url']
    last_char_is_slash = solr_core_url[-1] == '/'
    return solr_core_url if last_char_is_slash else solr_core_url + '/'


class GetPacsAccessionTask(luigi.Task):
    accession_number = luigi.Parameter()

    def run(self):
        # find on pacs
        query = cmd.add_accession(cmd.basic_query(), self.accession_number)
        results = exec.run(query)

        # save to json
        with self.output().open('w') as outfile:
            w.write_file(results, outfile)

    def output(self):
        json_path = get_json_path(self.accession_number)
        return luigi.LocalTarget(json_path)


class DeleteSolrAccessionTask(luigi.Task):
    accession_number = luigi.Parameter()

    def requires(self):
        GetPacsAccessionTask(accession_number=self.accession_number)

    def run(self):
        url = parse.urljoin(get_solr_core_url(), 'update')
        delete_response = requests.post(
            url=url,
            data='''
                   <delete>
                       <query>
                           AccessionNumber:{}
                       </query>
                   </delete>
                   '''.format(self.accession_number),
            headers={"Content-type": "text/xml"}
        )
        if not delete_response.ok:
            raise ValueError(delete_response.text)

        commit_response = requests.post(
            url=url,
            data='<commit />',
            headers={"Content-type": "text/xml"}
        )

        if not commit_response.ok:
            raise ValueError(commit_response.text)

        delete_success_path = os.path.join(
            status_dir,
            '{}_removed'.format(self.accession_number)
        )
        Path(delete_success_path).touch()

    def output(self):
        delete_success_path = os.path.join(
            status_dir,
            '{}_removed'.format(self.accession_number)
        )
        return luigi.LocalTarget(delete_success_path)


class UpdateSolrTask(luigi.Task):
    accession_number = luigi.Parameter()

    def requires(self):
        return DeleteSolrAccessionTask(accession_number=self.accession_number)

    def run(self):
        base_url = parse.urljoin(get_solr_core_url(), 'update/json')

        file_path = get_json_path(self.accession_number)
        print('FILE PATH: ', file_path)
        file = {base_url: open(file_path)}
        update_response = requests.post(url=base_url, files=file)

        print('UPDATE response:\n',update_response)
        if not update_response.ok:
            raise ValueError(update_response.text)

        update_success_path = os.path.join(
            status_dir,
            '{}_updated'.format(self.accession_number)
        )

        Path(update_success_path).touch()

    def output(self):
        update_success_path = os.path.join(
            status_dir,
            '{}_updated'.format(self.accession_number)
        )
        return luigi.LocalTarget(update_success_path)


class AccessionListUpdateTask(luigi.Task):
    csv_path = luigi.Parameter()
    success_path = os.path.join(
        status_dir,
        'task_succeeded_{}'.format(int(time.time()))
    )

    def run(self):
        accessions_df = pd.read_csv(self.csv_path)
        accessions_col = accessions_df.ix[:, 0]

        print('Accessions to UPDATE:', accessions_col, sep='\n')

        for accession_number in accessions_col:
            yield UpdateSolrTask(accession_number)

        pd.DataFrame([{'input_file': self.csv_path}]).to_csv(self.success_path)

    def output(self):
        return luigi.LocalTarget(self.success_path)


# example usage:
# PYTHONPATH='.' luigi --module tasks.update_accessions AccessionListUpdateTask --csv-path 'list.csv' --local-scheduler
if __name__ == '__main__':
    luigi.run()
