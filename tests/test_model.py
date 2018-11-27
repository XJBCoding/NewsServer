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
        self.test_model()

    def setUp(self):
        """called before the first test case of this unit begins"""
        self.a1 = Article('https://www.huffingtonpost.com/entry/ariana-grandes-thank-u-next-trailer-is-all-mean-girls-pete-davidson_us_5bfd49d4e4b0771fb6be205e')
        self.a1.build()


    def tearDown(self):
        """called after all test cases finish of this unit"""
        pass

    def test_model(self):
        assert self.a1.category == 'entertainment'
