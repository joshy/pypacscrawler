import shlex, subprocess
import dicom
import pandas as pd

START_DATE = '2016-01-01'
END_DATE = '2016-12-31'

MODALITIES = ['CT', 'MR', 'PT', 'CR', 'XA', 'SR', 'NM', 'MG', 'US', 'DX', 'RF',
              'OT', 'PR', 'KO', 'SC', 'SD', 'PX', 'xa', 'DR',]

def basic_query():
    return """
           findscu -to 6000 -S -k 0008,0052=SERIES -aec AE_ARCH2_4PR 10.5.66.74 104 -aet YETI
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
           -k SeriesInstanceUID
           -k StudyDate=20160101
           -k SeriesDate=20160101
           -k Modality=CT
           -k SeriesTime=000000-115959
           """


def add_modalitiy(query, modality):
    return query + ' -k Modality=' + modality


def add_date(query, date):
    return query + ' -k StudyDate=' + date + ' -k SeriesDate=' + date


def add_time(query, time):
    return query + ' -k SeriesTime=' + time


def run():

    cmd = shlex.split(args)
    completed = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    lines = completed.stderr.decode('latin1').splitlines()
    data = dicom.get_headers(lines)

    df = pd.DataFrame.from_dict(data)
    df.to_csv("data.csv", header=True, index=False)


if __name__ == '__main__':
    run():