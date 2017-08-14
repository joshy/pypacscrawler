import unittest

from pypacscrawler.dicom import _is_start_or_end, _get_tag, _get_value


class DicomTest(unittest.TestCase):
    def test_start(self):
        line = 'I:'
        start = _is_start_or_end(line)
        self.assertEqual(True, start)

    def test_tag(self):
        line = 'I: (0008,0060) CS [MR] #   2, 1 Modality'
        tag = _get_tag(line)
        self.assertEqual('Modality', tag)

    def test_value(self):
        line = 'I: (0008,0060) CS [MR] #   2, 1 Modality'
        tag = _get_value(line)
        self.assertEqual('MR', tag)
