import shlex
import subprocess

from typing import List, Dict
from pypacscrawler.dicom import get_results


def run(query):
    # type: (str) -> (List[Dict[str, str]], int)
    """
    Executes a findscu query and parses the result
    :param query: findscu query
    :return: a tuple where the first value is a list of DICOM tags and values
    and second value is result size
    """
    cmd = shlex.split(query)
    completed = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(cmd)
    lines = completed.stderr.decode('latin1')
    print(lines)
    result = get_results(lines)
    print(len(result))
    return result, len(result)
