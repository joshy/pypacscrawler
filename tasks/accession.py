import configparser
from itertools import chain

import luigi
import pypacscrawler.writer as w
from pypacscrawler.query import query_accession_number
from tasks.study_uid import StudyUIDTask

class AccessionTask(luigi.Task):
    # example run command
    # python -m tasks.accession AccessionTask --accession-number 1234 --local-scheduler
    accession_number = luigi.Parameter()

    def requires(self):
        return StudyUIDTask(self.accession_number)

    def run(self):
        config = configparser.ConfigParser()
        filename ='./instance/config.cfg'
        with open(filename) as fp:
            config.read_file(chain(['[PACS]'], fp), source=filename)
        with self.input().open('r') as f:
            study_uid = f.read()

        print('------------------------------------------------')
        print(study_uid)
        results = query_accession_number(config, study_uid)
        with self.output().open('w') as outfile:
            w.write_file(results, outfile)

    def output(self):
        return luigi.LocalTarget('data/%s_accession.json' % self.accession_number)


if __name__ == '__main__':
    luigi.run()
