""" This file contains the tasks to downlad the json files from
    the ris as well as the routines to upload these files to solr
"""

import logging
import os
import json
import requests
import luigi
from pypacscrawler.config import get_solr_upload_url
from pypacscrawler.convert import convert_pacs_file, merge_pacs_ris
from tasks.day import DayTask


class ConvertPacsFile(luigi.Task):
    day = luigi.Parameter()

    def requires(self):
        return DayTask(self.day)

    def run(self):
        with self.input().open('r') as daily:
            data = daily.read()
            json_in = json.loads(data)

        json_out = convert_pacs_file(json_in)

        with self.output().open('w') as my_dict:
            json.dump(json_out, my_dict, indent=4)

    def output(self):
        return luigi.LocalTarget('data/%s_pacs_converted.json' % self.day)



class MergePacsRis(luigi.Task):
    day = luigi.Parameter()

    def requires(self):
        return ConvertPacsFile(self.day)

    def run(self):
        with self.input().open('r') as daily:
            data = daily.read()
            pacs_in = json.loads(data)

        merged_out = merge_pacs_ris(pacs_in)

        with self.output().open('w') as my_dict:
            json.dump(merged_out, my_dict, indent=4)

    def output(self):
        return luigi.LocalTarget('data/%s_ris_pacs_merged.json' % self.day)


class DailyUpConvertedMerged(luigi.Task):
    day = luigi.Parameter()

    def requires(self):
        return MergePacsRis(self.day)

    def run(self):
        upload_url = get_solr_upload_url()
        logging.debug('Uploading to url %s', upload_url)
        with self.input().open('rb') as in_file:
            file = {
                'file': (
                    in_file.name,
                    in_file,
                    'application/json'
                )
            }
            update_response = requests.post(
                url=upload_url,
                files=file,
                params={'commit': 'true'}
            )

        if not update_response.ok:
            update_response.raise_for_status()
        else:
            with self.output().open('w') as my_file:
                my_file.write('Upload successful')

    def output(self):
        return luigi.LocalTarget('data/%s_solr_uploaded.txt' % self.day)


# example usage:
# PYTHONPATH='.' luigi --module tasks.ris_pacs_merge_upload DailyUpConvertedMerged --local-scheduler --day yyyy-mm-dd
if __name__ == '__main__':
    luigi.run()
