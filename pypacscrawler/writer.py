
import logging
import os
import json
import pandas as pd

from typing import Dict, List
from pypacscrawler.transform import transform

OUTPUT_DIR = 'data'


def _get_file_name(month: str, day: str, mod: str):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    file_name = os.path.join(OUTPUT_DIR, 'data-')
    if month:
        return file_name + month + '.json'
    else:
        return file_name + day + '-' + mod + '.json'


def write_results(results: List[Dict[str, str]], month: str, day: str, mod: str):
    file_name = _get_file_name(month, day, mod)
    frames = pd.concat([pd.DataFrame(x) for x in results if len(x) > 0])
    dfs = transform(frames)
    logging.info('Writing results to file %s', file_name)
    with open(file_name, 'w', encoding='ISO-8859-1') as out:
        json.dump(dfs, out)
