import luigi
import configparser

import pypacscrawler.writer as w
from pypacscrawler.query import query_accession_number


class AccessionTask(luigi.Task):
    # example run command
    # python -m tasks.accession AccessionTask --accession-number 1234 --local-scheduler
    accession_number = luigi.Parameter()

    def run(self):
        config = configparser.ConfigParser()
        config.read_file(open('config.ini'))
        results = query_accession_number(config, self.accession_number)
        with self.output().open('w') as outfile:
            w.write_file(results, outfile)

    def output(self):
        return luigi.LocalTarget('data/%s_accession.json' % self.accession_number)


if __name__ == '__main__':
    luigi.run()