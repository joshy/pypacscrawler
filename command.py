import shlex
import pandas as pd

from datetime import date


MODALITIES = ['CT', 'MR', 'PT', 'CR', 'XA', 'SR', 'NM', 'MG', 'US', 'DX', 'RF',
              'OT', 'PR', 'KO', 'SC', 'SD', 'PX', 'xa', 'DR']

TIME_RANGES = ['000000-075959',
               '080000-095959',
               '100000-115959',
               '120000-135959',
               '140000-155959',
               '160000-175959',
               '180000-235959']


def _basic_query():
    return 'findscu -to 6000 -v -S \
           -k 0008,0052=SERIES \
           -aec AE_ARCH2_4PR 10.5.66.74 104 \
           -aet YETI \
           -k PatientName \
           -k PatientBirthDate  \
           -k PatientID \
           -k PatientSex \
           -k StudyID \
           -k StudyDate \
           -k Modality \
           -k AccessionNumber \
           -k BodyPartExamined \
           -k StudyDescription \
           -k SeriesDescription \
           -k SeriesNumber \
           -k InstanceNumber \
           -k ReferringPhysicianName \
           -k InstitutionName \
           -k StudyInstanceUID \
           -k SeriesInstanceUID'


def _add_modality(query, modality):
    return query + ' -k Modality=' + modality


def _add_date(query, date):
    q_date = date.strftime("%Y%m%d")
    return query + ' -k StudyDate=' + q_date + ' -k SeriesDate=' + q_date


def _add_time(query, time):
    return query + ' -k SeriesTime=' + time


def _year_start_end(year):
    start = date(year.year, 1, 1)
    end = date(year.year, 12, 31)
    return start, end


def create_cmds(date, mod):
    """ Creates commands for a specific date and modality. """
    cmds = []
    basic = _basic_query()
    with_date = _add_date(basic, date)
    for time_range in TIME_RANGES:
        with_time = _add_time(with_date, time_range)
        args = _add_modality(with_time, mod)
        cmds.append(shlex.split(args))
    return cmds


def create_full_year_cmds(year):
    """
    Generates all the findscu commands for all modalities for
    all the days of the year.
    """
    cmds = []
    basic = _basic_query()
    start, end = _year_start_end(year)
    for day in pd.date_range(start, end):
        day_p = _add_date(basic, day)
        for time_range in TIME_RANGES:
            time_p = _add_time(day_p, time_range)
            for mod in MODALITIES:
                args = _add_modality(time_p, mod)
                cmds.append(shlex.split(args))
    return cmds
