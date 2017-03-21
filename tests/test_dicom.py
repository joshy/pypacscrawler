import unittest

from pypacscrawler import dicom


class DicomTest(unittest.TestCase):
    def test_start(self):
        line = 'W:'
        start = dicom._is_start_or_end(line)
        self.assertEqual(True, start)

    def test_tag(self):
        line = 'W: (0008,0060) CS [MR] #   2, 1 Modality'
        tag = dicom._get_tag(line)
        self.assertEqual('Modality', tag)

    def test_value(self):
        line = 'W: (0008,0060) CS [MR] #   2, 1 Modality'
        tag = dicom._get_value(line)
        self.assertEqual('MR', tag)
