"""
This test checks parsing functionality of the Article class
"""
import os
import sys
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import unittest
import requests
from Article import Article


class ModelTestCase(unittest.TestCase):
    def runTest(self):
        self.test_url()
        self.test_source_url()
        self.test_download_html()
        self.test_parse_html()

    def setUp(self):
        """called before the first test case of this unit begins"""
        self.a1 = Article(
            'www.cnn.com/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html')
        self.a1.build()


    def tearDown(self):
        """called after all test cases finish of this unit"""
        pass

    def test_model(self):
        assert self.a1.category == 'sport'
