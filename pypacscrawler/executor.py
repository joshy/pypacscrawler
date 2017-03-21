import subprocess
from pypacscrawler.dicom import get_results


def run(query):
    # type: (str) -> (List[Dict[str, str]], int)
    """
    Executes a findscu query and parses the result
    :param query: findscu query
    :return: a tuple where the first value is a list of dicom tags and values
    and second value is result size
    """
    completed = subprocess.run(query, stderr=subprocess.PIPE)
    lines = completed.stderr.decode('latin1').splitlines()
    result = get_results(lines)
    return result, len(result)
