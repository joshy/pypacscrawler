import os
import pandas as pd

OUTPUT_DIR = 'data'


def get_file_name(month: str, day: str, mod: str):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    file_name = os.path.join(OUTPUT_DIR, 'data-')
    if month:
        return file_name + month + '.csv'
    else:
        return file_name + day + '-' + mod + '.csv'


def write_results(results, file_name):
    frames = pd.concat([pd.DataFrame(x) for x in results if len(x) > 0])
    frames.to_csv(file_name, header=True, index=False, sep=';')
