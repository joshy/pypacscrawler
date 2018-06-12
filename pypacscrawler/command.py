from datetime import date, datetime
from typing import Tuple

from pypacscrawler.config import pacs_settings


MODALITIES = ['CT', 'MR', 'PT', 'CR', 'XA', 'SR', 'NM', 'MG', 'US', 'DX', 'RF',
              'OT', 'PR', 'KO', 'SC', 'SD', 'PX', 'xa', 'DR']

INITIAL_TIME_RANGE = '000000-235959'


def basic_query(app):
    """Returns a basic findscu command with no query parameters set."""
    return '''findscu -to 6000 -v -S -k 0008,0052=SERIES {}
           -k PatientName
           -k PatientBirthDate
           -k PatientID
           -k PatientSex
           -k StudyID
           -k StudyDate
           -k Modality
           -k AccessionNumber
           -k BodyPartExamined
           -k StudyDescription
           -k SeriesDescription
           -k SeriesNumber
           -k InstanceNumber
           -k ReferringPhysicianName
           -k InstitutionName
           -k StudyInstanceUID
           -k SeriesInstanceUID'''.format(pacs_settings(app))


def add_modality(query, modality):
    """ Adds the modality to the query. """
    return query + ' -k Modality=' + modality


def add_day(query, day):
    """ Adds the StudyDate and SeriesDate to the query. """
    q_day = day.strftime("%Y%m%d")
    return query + ' -k StudyDate=' + q_day + ' -k SeriesDate=' + q_day


def add_time(query, time):
    """ Adds the Series time to the query. """
    return query + ' -k SeriesTime=' + time


def add_accession_number(query, accession_number):
    """ Limit by Accession Number """
    return query + ' -k AccessionNumber=' + accession_number


def year_start_end(year):
    # type: (str) -> Tuple[date, date]
    y = datetime.strptime(year, '%Y')
    start = date(y.year, 1, 1)
    end = date(y.year, 12, 31)
    return start, end
