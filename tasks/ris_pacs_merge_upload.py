""" This file contains the routines to downlad the json files from
    the ris as well as the routines to upload these files to solr
"""

import logging
import os
import json
import requests
import luigi
from pypacscrawler.config import get_report_show_url
from tasks.day import DayTask


class ConvertPacsFile(luigi.Task):
    day = luigi.Parameter()

    def requires(self):
        return DayTask(self.day)

    def run(self):
        with self.input().open('r') as daily:
            data = daily.read()
            json_in = json.loads(data)

        json_out = convert_pacs_file(json_in)

        with self.output().open('w') as my_dict:
            json.dump(json_out, my_dict, indent=4)

    def output(self):
        return luigi.LocalTarget('data/pacs_converted_%s.json' % self.day)



class MergePacsRis(luigi.Task):
    day = luigi.Parameter()

    def requires(self):
        return ConvertPacsFile(self.day)

    def run(self):
        with self.input().open('r') as daily:
            data = daily.read()
            pacs_in = json.loads(data)

        merged_out = merge_pacs_ris(pacs_in)

        with self.output().open('w') as my_dict:
            json.dump(merged_out, my_dict, indent=4)

    def output(self):
        return luigi.LocalTarget('data/ris_pacs_merged_%s.json' % self.day)


def convert_pacs_file(json_in):
    """ Convert: pacs_date.json -> pacs_convert_date.json
        The converted file contains only one entry per accession number
        structured into one parent and one child for each series
    """
    my_dict = []
    flag = 0
    acc_num = []
    for entry in json_in:
        if entry['AccessionNumber'] not in acc_num:
            acc_num.append(entry['AccessionNumber'])
            if flag == 0:
                p_dict = {}
            else:
                my_dict.append(p_dict)
                p_dict = {}

            p_dict['Category'] = 'parent'
            if entry["AccessionNumber"]:
                p_dict["AccessionNumber"] = entry["AccessionNumber"]
            if entry["InstanceAvailability"]:
                p_dict["InstanceAvailability"] = entry["InstanceAvailability"]
            if entry["InstitutionName"]:
                p_dict["InstitutionName"] = entry["InstitutionName"]
            if entry["Modality"]:
                p_dict["Modality"] = entry["Modality"]
            if entry["PatientBirthDate"]:
                p_dict["PatientBirthDate"] = entry["PatientBirthDate"]
            if entry["PatientID"]:
                p_dict["PatientID"] = entry["PatientID"]
            if entry["PatientName"]:
                p_dict["PatientName"] = entry["PatientName"]
            if entry["PatientSex"]:
                p_dict["PatientSex"] = entry["PatientSex"]
            if entry["ReferringPhysicianName"]:
                p_dict["ReferringPhysicianName"] = entry["ReferringPhysicianName"]
            if entry["SeriesDate"]:
                p_dict["SeriesDate"] = entry["SeriesDate"]
            if entry["SpecificCharacterSet"]:
                p_dict["SpecificCharacterSet"] = entry["SpecificCharacterSet"]
            if entry["StudyDate"]:
                p_dict["StudyDate"] = entry["StudyDate"]
            if entry["StudyDescription"]:
                p_dict["StudyDescription"] = entry["StudyDescription"]
            if entry["StudyID"]:
                p_dict["StudyID"] = entry["StudyID"]
            if entry["StudyInstanceUID"]:
                p_dict["StudyInstanceUID"] = entry["StudyInstanceUID"]
                p_dict["id"] = entry["StudyInstanceUID"]
            p_dict['_childDocuments_'] = []
            p_dict = add_child(p_dict, entry)
            flag = 1

        else:
            p_dict = add_child(p_dict, entry)

    return my_dict


def add_child(parent, entry):
    """ add child entry """
    child_dict = {}
    child_dict['Category'] = 'child'
    if entry["BodyPartExamined"]:
        child_dict["BodyPartExamined"] = entry["BodyPartExamined"]
    if entry["SeriesDescription"]:
        child_dict["SeriesDescription"] = entry["SeriesDescription"]
    if entry["SeriesInstanceUID"]:
        child_dict["SeriesInstanceUID"] = entry["SeriesInstanceUID"]
    if entry["SeriesInstanceUID"]:
        child_dict["id"] = entry["SeriesInstanceUID"]
    if entry["SeriesNumber"]:
        child_dict["SeriesNumber"] = entry["SeriesNumber"]
    if entry["SeriesTime"]:
        child_dict["SeriesTime"] = entry["SeriesTime"]
    parent['_childDocuments_'].append(child_dict)
    return parent


def merge_pacs_ris(pacs):
    """ Inssert ris report into converted pacs json file"""
    my_dict = []

    for entry in pacs:
        dic = {}
        dic = entry
        aNum = str(entry['AccessionNumber'])
        url = get_report_show_url() + aNum + '&output=text'
        response = requests.get(url)
        data = response.text
        dic['RisReport'] = data
        my_dict.append(dic)

    return my_dict



class DailyUpConvertedMerged(luigi.Task):
    url = luigi.Parameter()
    day = luigi.Parameter()

    def requires(self):
        return MergePacsRis(self.day)

    def run(self):
        logging.debug('Uploading to url %s', self.url)
        headers = {'content-type': 'application/json'}
        params = {'commit': 'true'}
        payload = self.input().open('rb').read()
        r = requests.post(self.url, data=payload, params=params, headers=headers)
        if r.status_code == requests.codes.ok:
            with self.output().open('w') as outfile:
                outfile.write('DONE')

    def output(self):
        day_file = os.path.basename(self.input().path)
        return luigi.LocalTarget('data/%s.uploaded_day' % day_file)


# example usage:
# PYTHONPATH='.' luigi --module tasks.ris_pacs_merge_upload DailyUpConvertedMerged --local-scheduler --day yyyy-mm-dd
if __name__ == '__main__':
    luigi.run()
