import os
import sys
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import tempfile
from flask import url_for
from news_server import create_app
import pytest
import unittest
from datetime import date,timedelta


class FlaskClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

        self.app.config['SECRET_KEY'] = 'sekrit!'

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        self.user_with_history = 'testing_username_with_history'
        self.user_no_history = 'testing_username_no_history'

    def tearDown(self):
        self.app_context.pop()

    '''
    This is a test to make sure that the user cannot view analytics without logging in
    '''
    def test_add_history_login(self):
        resp = self.client.post('/add-history')
        assert b'You are not logged in' in resp.data

    def test_add_history(self):
        username = self.user_with_history

        user_history = self.app.db["user_history"]
        user_history.remove({'username':username})  # clear history from previous tests

        with self.client.session_transaction() as sess:
            sess['username'] = username

        resp = self.client.post('/add-history', data={'mins': 10, 'category': 'health', 'url': '#'})
        # need to assert that the data is in MongoDB
        assert b'Added article to DB' in resp.data

    # def test_analytics_time(self):
    #     # TODO: after setting up MongoDB code, need to pass dummy data in database
    #     with self.client.session_transaction() as sess:
    #         sess['username'] = 'testing'
    #     resp = self.client.get('/analytics')
    #     assert b'mins' or b'minutes' in resp.data