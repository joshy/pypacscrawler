import logging
import os

import luigi
import requests

from tasks.month import MonthTask


class UploadTask(luigi.Task):
    url = luigi.Parameter()
    month = luigi.Parameter()

    def requires(self):
        return MonthTask(month=self.month)

    def run(self):
        logging.debug('Uploading to url %s', self.url)
        headers = {'content-type': 'application/json'}
        params = {'commit': 'true'}
        payload = self.input().open('rb').read()
        r = requests.post(self.url, data=payload, params=params, headers=headers)
        if r.status_code == requests.codes.ok:
            with self.output().open('w') as outfile:
                outfile.write('DONE')
        else:
            r.raise_for_status()

    def output(self):
        month_file = os.path.basename(self.input().path)
        return luigi.LocalTarget('data/%s.uploaded' % month_file)


if __name__ == '__main__':
    luigi.run()
