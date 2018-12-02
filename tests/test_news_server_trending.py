import os
import sys
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import tempfile
from flask import url_for, request, Response, session
from news_server import create_app, trending
import pytest
import unittest


class FlaskClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

        self.app.config['SECRET_KEY'] = 'sekrit!'

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    '''
    This is a test to make sure that the user cannot search without logging in
    '''
    def test_trending(self):
        resp = trending()
        self.assertTrue(resp)