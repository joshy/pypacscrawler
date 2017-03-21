import shlex
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
    cmd = shlex.split(query)
    print('running command', cmd)
    completed = subprocess.run(cmd, stderr=subprocess.PIPE)
    lines = completed.stderr.decode('latin1').splitlines()
    result = get_results(lines)
    print('got {} results'.format(len(result)))
    return result, len(result)
