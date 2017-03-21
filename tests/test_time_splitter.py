import unittest

from pypacscrawler import time_splitter

INITIAL = '000000-235959'


class TimeSplitterTest(unittest.TestCase):
    def test_simple(self):
        l, r = time_splitter.split(INITIAL)
        self.assertEqual('000000-115959', l)
        self.assertEqual('120000-235959', r)

    def test_second_level(self):
        left, right = time_splitter.split(INITIAL)
        l1, l2 = time_splitter.split(left)
        self.assertEqual('000000-055959', l1)
        self.assertEqual('060000-115959', l2)

    def test_one_error_case(self):
        l, r = time_splitter.split('060000-115959')
        self.assertEqual('060000-085959', l)
        self.assertEqual('090000-115959', r)


    def test_third_level(self):
        # 0-3, 3-6, 6-9, 9-12
        left, right = time_splitter.split(INITIAL)
        l, r = time_splitter.split(left)
        ll, lr = time_splitter.split(l)
        rl, rr = time_splitter.split(r)
        self.assertEqual('000000-025959', ll)
        self.assertEqual('030000-055959', lr)
        #self.assertEqual('060000-085959', rl)
        self.assertEqual('090000-115959', rr)


    def test_right(self):
        left, right = time_splitter.split(INITIAL)
        l, r = time_splitter.split(left)
        ll, lr = time_splitter.split(l)
        ll, _ = time_splitter.split(l)
        lll, rrr = time_splitter.split(ll)
        llll, rrrr = time_splitter.split(lll)
        self.assertEqual('000000-012959', lll)
        self.assertEqual('013000-025959', rrr)
        self.assertEqual('000000-004459', llll)
        self.assertEqual('004500-012959', rrrr)

