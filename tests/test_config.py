import os
import unittest

from flask import Flask
from pypacscrawler import config


class ConfigTest(unittest.TestCase):
    def test_simple(self):
        app = Flask(__name__)
        app.config.from_object('pypacscrawler.default_config')
        app.config.from_pyfile('config.cfg')
        settings = config.pacs_settings(app)
        self.assertEqual("-aec AE_CALLED 127.0.0.1 104 -aet AE_TITLE",
                         settings)

