import os
import unittest

from pypacscrawler.config import pacs_settings


class ConfigTest(unittest.TestCase):
    def test_simple(self):
        settings = pacs_settings(file='config.ini.template')
        self.assertEqual("-aec AE_CALLED 127.0.0.1 104 -aet AE_TITLE",
                         settings)

