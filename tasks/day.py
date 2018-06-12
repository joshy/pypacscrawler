import luigi
from luigi.format import UTF8, Text, TextFormat

import pypacscrawler.writer as w
from pypacscrawler.query import query_day


class DayTask(luigi.Task):
    # example run command
    # python -m tasks.day DayTask --day 2017-01-01 --local-scheduler
    # day format is yyyy-mm-dd
    day = luigi.Parameter()

    def run(self):
        results = query_day(self.day)
        with self.output().open('w') as outfile:
            w.write_file(results, outfile)

    def output(self):
        return luigi.LocalTarget('data/%s_pacs.json' % self.day)


if __name__ == '__main__':
    luigi.run()