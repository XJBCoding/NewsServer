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
import pymongo


class FlaskClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

        self.app.config['SECRET_KEY'] = 'sekrit!'

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        mongo_client = pymongo.MongoClient("mongodb+srv://news:123@cluster0-avowj.mongodb.net/test?retryWrites=true")
        self.db = mongo_client["newsapp"]

        self.user_with_history = 'testing_username_with_history'
        self.user_no_history = 'testing_username_no_history'

    def tearDown(self):
        self.app_context.pop()

    def test_add_history(self):
        username = self.user_with_history
        user_history = self.db["user_history"]
        user_history.remove({'username':username})  # clear history from previous tests

        with self.client.session_transaction() as sess:
            sess['username'] = username

        resp = self.client.post('/add-history', data={'mins': 10, 'category': 'health', 'url': '#'})
        # need to assert that the data is in MongoDB
        assert b'Added article to DB' in resp.data

    def test_analytics_time_with_history(self):
        username = self.user_with_history
        user_history = self.db["user_history"]

        with self.client.session_transaction() as sess:
            sess['username'] = username

        resp = self.client.get('/analytics')
        assert b'10 min' in resp.data

    def test_analytics_topic_with_history(self):
        username = self.user_with_history
        user_history = self.db["user_history"]

        with self.client.session_transaction() as sess:
            sess['username'] = username

        resp = self.client.get('/analytics')
        assert b'health' in resp.data

    def test_analytics_no_history(self):
        username = self.user_no_history
        user_history = self.db["user_history"]

        with self.client.session_transaction() as sess:
            sess['username'] = username

        resp = self.client.get('/analytics')
        assert not b'mins' in resp.data

    