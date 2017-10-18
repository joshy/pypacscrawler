import luigi

import pypacscrawler.writer as w
from pypacscrawler.query import query_month


class MonthTask(luigi.Task):
    # month format is yyyy-mm
    month = luigi.Parameter()

    def run(self):
        results = query_month(self.month)
        with self.output().open('w') as outfile:
            w.write_file(results, outfile)

    def output(self):
        return luigi.LocalTarget('data/%s.json' % self.month)


if __name__ == '__main__':
    luigi.run()