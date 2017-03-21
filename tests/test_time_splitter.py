import unittest

from pypacscrawler import time_splitter

INITIAL = '000000-235959'


class TimeSplitterTest(unittest.TestCase):
    def test_simple(self):
        split = time_splitter.split(INITIAL)
        self.assertEqual(('000000-115959', '120000-235959'), split)

    def test_other(self):
        left, right = time_splitter.split(INITIAL)
        l1, l2 = time_splitter.split(left)
        self.assertEqual('000000-055959', l1)
        self.assertEqual('060000-115959', l2)

    def test_other_one(self):
        left, _ = time_splitter.split(INITIAL)
        l, _ = time_splitter.split(left)
        ll, _ = time_splitter.split(l)
        lll, rrr = time_splitter.split(ll)
        llll, rrrr = time_splitter.split(lll)
        self.assertEqual('000000-012959', lll)
        self.assertEqual('013000-025959', rrr)
        self.assertEqual('000000-004459', llll)
        self.assertEqual('004500-012959', rrrr)
