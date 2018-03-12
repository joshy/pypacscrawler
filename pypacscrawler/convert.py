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
            acc_dict[entry['AccessionNumber']] = p_dict
        else:
            p_dict = acc_dict[entry['AccessionNumber']]
            p_dict = add_child(p_dict, entry)

    return acc_dict.values()


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