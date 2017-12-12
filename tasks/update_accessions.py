import luigi
import pandas as pd
import requests
from urllib import parse
from pathlib import Path
import pypacscrawler.command as cmd
import pypacscrawler.executor as exec
from pypacscrawler.config import get_solr_core_url
import pypacscrawler.writer as w
import time
import os


class CreateOutputDirTask(luigi.Task):

    def run(self):
        if not os.path.exists(self.output().path):
            os.makedirs(self.output().path)

    def output(self):
        return luigi.LocalTarget(os.path.join('data', 'status'))


class GetPacsAccessionTask(luigi.Task):
    accession_number = luigi.Parameter()

    def requires(self):
        return CreateOutputDirTask()

    def run(self):
        # find on pacs
        query = cmd.add_accession(cmd.basic_query(), self.accession_number)
        results, _ = exec.run(query)

        # save to json
        with self.output().open('w') as outfile:
            w.write_file([results], outfile)

    def output(self):
        file_path_no_ext = os.path.join(
            self.input().path,
            self.accession_number
        )
        json_path = '{}.json'.format(file_path_no_ext)
        return luigi.LocalTarget(json_path)


class DeleteSolrAccessionTask(luigi.Task):
    accession_number = luigi.Parameter()

    def requires(self):
        return CreateOutputDirTask()

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
            headers={"Content-type": "text/xml"},
            params={"commit": "true"}
        )
        if not delete_response.ok:
            raise ValueError(delete_response.text)

        Path(self.output().path).touch()

    def output(self):
        delete_success_path = os.path.join(
            self.input().path,
            '{}_removed'.format(self.accession_number)
        )
        return luigi.LocalTarget(delete_success_path)


class UpdateSolrTask(luigi.Task):
    accession_number = luigi.Parameter()

    def requires(self):
        return {
            'solr_delete': DeleteSolrAccessionTask(
                accession_number=self.accession_number
            ),
            'get_pacs': GetPacsAccessionTask(
                accession_number=self.accession_number,
            ),
            'status_dir': CreateOutputDirTask()
        }

    def run(self):
        base_url = parse.urljoin(get_solr_core_url(), 'update/json')
        input_json = self.input()['get_pacs']
        with input_json.open('rb') as in_file:
            file = {
                base_url: (
                    in_file.name,
                    in_file,
                    'application/json'
                )
            }
            update_response = requests.post(
                url=base_url,
                files=file,
                params={'commit': 'true'}
            )

        if not update_response.ok:
            raise ValueError(update_response.text)

        Path(self.output().path).touch()

    def output(self):
        update_success_path = os.path.join(
            self.input()['status_dir'].path,
            '{}_updated'.format(self.accession_number)
        )
        return luigi.LocalTarget(update_success_path)


class AccessionListUpdateTask(luigi.Task):
    csv_path = luigi.Parameter()

    def requires(self):
        return CreateOutputDirTask()

    def run(self):
        accessions_df = pd.read_csv(self.csv_path)
        accessions_col = accessions_df.ix[:, 0]

        for accession_number in accessions_col:
            yield UpdateSolrTask(str(accession_number))

        success_path = self.output().path

        pd.DataFrame([{'input_file': self.csv_path}]).to_csv(success_path)

    def output(self):
        output_path = os.path.join(
            self.input().path,
            'task_succeeded_{}'.format(int(time.time()))
        )
        return luigi.LocalTarget(output_path)


# example usage:
# PYTHONPATH='.' luigi --module tasks.update_accessions AccessionListUpdateTask --csv-path 'list.csv' --local-scheduler
if __name__ == '__main__':
    luigi.run()
