import unittest
from pathlib import Path
import json
import pandas as pd

from pypacscrawler.convert import convert_pacs_file

sample_json = Path.cwd() / 'tests' / 'test_json'

class ConvertTest(unittest.TestCase):

    def setUp(self):
        with sample_json.open() as f:
            self.raw_data = json.load(f)
            self.data = convert_pacs_file(self.raw_data)

    def test_setup(self):
        self.assertEqual(5515, len(self.raw_data))


    def test_conv(self):
        df_raw = pd.DataFrame.from_dict(self.raw_data)
        acc_example = len(df_raw[df_raw['AccessionNumber'] == '25687728'])
        study = [d for d in self.data if d['AccessionNumber'] == '25687728'][0]
        series = study['_childDocuments_']
        self.assertEqual(acc_example, len(series))