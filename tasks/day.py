import luigi
import pypacscrawler.writer as w
from pypacscrawler.query import query_day
from tasks.util import load_config


class DayTask(luigi.Task):
    # example run command
    # python -m tasks.day DayTask --day 2017-01-01 --local-scheduler
    # day format is yyyy-mm-dd
    day = luigi.Parameter()

    def run(self):
        config = load_config()
        results = query_day(config, self.day)
        with self.output().open('w') as outfile:
            w.write_file(results, outfile)

    def output(self):
        return luigi.LocalTarget('data/%s_pacs.json' % self.day)


if __name__ == '__main__':
    luigi.run()
