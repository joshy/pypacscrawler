import shlex
import pandas as pd

from datetime import date

from pypacscrawler.config import pacs_settings


MODALITIES = ['CT', 'MR', 'PT', 'CR', 'XA', 'SR', 'NM', 'MG', 'US', 'DX', 'RF',
              'OT', 'PR', 'KO', 'SC', 'SD', 'PX', 'xa', 'DR']

INITIAL_TIME_RANGE = '000000-235959'

TIME_RANGES = ['000000-075959',
               '080000-095959',
               '100000-115959',
               '120000-135959',
               '140000-155959',
               '160000-175959',
               '180000-235959']


def scout_query():
    """
    A minimal query just to find out the result size. If the size is below
    500, do the actual query.
    :return: minimal query
    """
    return '''findscu -to 6000 -v -S -k 0008,0052=SERIES {}
           -k AccessionNumber
           '''.format(pacs_settings())


def _basic_query():
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
           -k SeriesInstanceUID'''.format(pacs_settings())


def _add_modality(query, modality):
    return query + ' -k Modality=' + modality


def add_day(query, day):
    q_day = day.strftime("%Y%m%d")
    return query + ' -k StudyDate=' + q_day + ' -k SeriesDate=' + q_day


def add_time(query, time):
    return query + ' -k SeriesTime=' + time


def _year_start_end(year):
    start = date(year.year, 1, 1)
    end = date(year.year, 12, 31)
    return start, end


def create_cmds(day, mod):
    """ Creates commands for a specific day and modality. """
    cmds = []
    basic = _basic_query()
    with_day = add_day(basic, day)
    for time_range in TIME_RANGES:
        with_time = add_time(with_day, time_range)
        args = _add_modality(with_time, mod)
        cmds.append(shlex.split(args))
    return cmds


def create_year_month_cmds(year_month):
    """
    Generates all the findscu commands for all modalities for
    all the days of month.
    """
    cmds = []
    basic = _basic_query()
    start = year_month
    end = year_month + pd.tseries.offsets.MonthEnd()
    for day in pd.date_range(start, end):
        day_p = add_day(basic, day)
        for time_range in TIME_RANGES:
            time_p = add_time(day_p, time_range)
            for mod in MODALITIES:
                args = _add_modality(time_p, mod)
                cmds.append(shlex.split(args))
    return cmds


def create_full_year_cmds(year):
    start, end = _year_start_end(year)
    # MS is month start frequency
    months = pd.date_range(start, end, freq='MS')
    return [create_year_month_cmds(month) for month in months], months
