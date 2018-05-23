""" This file contains the locic associated with the tasks
    in the file 'ris_pacs_merge_upload.py'
"""

import requests
from datetime import datetime, date
from pypacscrawler.config import get_report_show_url


def convert_pacs_file(json_in):
    """ Convert: pacs_date.json -> pacs_convert_date.json
        The converted file contains only one entry per accession number
        structured into one parent and one child for each series
    """
    acc_dict = {}
    for entry in json_in:
        if entry['AccessionNumber'] not in acc_dict:
            p_dict = {}
            p_dict['Category'] = 'parent'
            if (entry["AccessionNumber"] and entry["PatientID"]):
                p_dict["AccessionNumber"] = entry["AccessionNumber"]
                p_dict["PatientID"] = entry["PatientID"]
                p_dict["id"] = entry["PatientID"] + '-' + entry["AccessionNumber"]
            if entry["InstanceAvailability"]:
                p_dict["InstanceAvailability"] = entry["InstanceAvailability"]
            if entry["InstitutionName"]:
                p_dict["InstitutionName"] = entry["InstitutionName"]
            if entry["Modality"]:
                p_dict["Modality"] = entry["Modality"]
            if (entry["PatientBirthDate"] and entry["SeriesDate"]):
                p_dict["PatientBirthDate"] = entry["PatientBirthDate"]
                p_dict["SeriesDate"] = entry["SeriesDate"]
                today = datetime.strptime(entry["SeriesDate"], "%Y%m%d")
                birthdate = datetime.strptime(entry["PatientBirthDate"], "%Y%m%d")
                p_dict["PatientAge"] = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            if entry["PatientName"]:
                p_dict["PatientName"] = entry["PatientName"]
            if entry["PatientSex"]:
                p_dict["PatientSex"] = entry["PatientSex"]
            if entry["ReferringPhysicianName"]:
                p_dict["ReferringPhysicianName"] = entry["ReferringPhysicianName"]
            if entry["SpecificCharacterSet"]:
                p_dict["SpecificCharacterSet"] = entry["SpecificCharacterSet"]
            if entry["StudyDate"]:
                p_dict["StudyDate"] = entry["StudyDate"]
            if entry["StudyDescription"]:
                p_dict["StudyDescription"] = entry["StudyDescription"]
            if entry["StudyID"]:
                p_dict["StudyID"] = entry["StudyID"]
            p_dict['_childDocuments_'] = []
            p_dict = add_child(p_dict, entry)
            acc_dict[entry['AccessionNumber']] = p_dict
        else:
            p_dict = acc_dict[entry['AccessionNumber']]
            p_dict = add_child(p_dict, entry)

    return list(acc_dict.values())


def add_child(parent, entry):
    """ add child entry """
    child_dict = {}
    child_dict['Category'] = 'child'
    if entry["BodyPartExamined"]:
        child_dict["BodyPartExamined"] = entry["BodyPartExamined"]
    if entry["SeriesDescription"]:
        child_dict["SeriesDescription"] = entry["SeriesDescription"]
    if entry["StudyInstanceUID"]:
        child_dict["StudyInstanceUID"] = entry["StudyInstanceUID"]
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