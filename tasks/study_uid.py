import configparser
from itertools import chain

import luigi
import pypacscrawler.writer as w
from pypacscrawler.query import query_for_study_uid


class StudyUIDTask(luigi.Task):
    # example run command
    # python -m tasks.accession AccessionTask --accession-number 1234 --local-scheduler
    accession_number = luigi.Parameter()

    def run(self):
        config = configparser.ConfigParser()
        filename ='./instance/config.cfg'
        with open(filename) as fp:
            config.read_file(chain(['[PACS]'], fp), source=filename)
        study_uid = query_for_study_uid(config, self.accession_number)
        with self.output().open('w') as outfile:
            outfile.write(study_uid)

    def output(self):
        return luigi.LocalTarget('data/%s_accession.txt' % self.accession_number)


if __name__ == '__main__':
    luigi.run()
