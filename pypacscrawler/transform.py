import os
import glob
import json

import pandas as pd
import numpy as np

def transform(df):
    g = df.groupby('StudyInstanceUID')

    drops = ['BodyPartExamined', 'SeriesDate', 'SeriesTime', 'SeriesNumber',
             'SeriesDescription', 'SeriesInstanceUID']
    results = []
    for name, group in g:
        # take the first row, doesn't matter because data is equal across
        # all rows in the group
        row = group.iloc[0].astype(str).to_dict()
        # Remove those because they should be in the series list
        [row.pop(d, None) for d in drops]
        # get the series as dictionaries
        series = group[['SeriesDate', 'SeriesNumber', 'SeriesDescription',
                        'SeriesTime', 'SeriesInstanceUID']]
        series = series.replace(np.nan, '', regex=True)
        series['id'] = series['SeriesInstanceUID']
        series['type'] = 'series'
        # attach it
        row['_childDocuments_'] = series.to_dict(orient="records")
        row['type'] = 'study'
        results.append(row)
    return results
