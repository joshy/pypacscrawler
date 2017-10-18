import luigi

import pypacscrawler.writer as w
from pypacscrawler.query import query_day

class DayTask(luigi.Task):
    # day format is yyyy-mm-dd
    day = luigi.Parameter()

    def run(self):
        results = query_day(self.day)
        with self.output().open('w') as outfile:
            w.write_file(results, outfile)

    def output(self):
        return luigi.LocalTarget('data-%s.json' % self.day)

if __name__ == '__main__':
    luigi.run()