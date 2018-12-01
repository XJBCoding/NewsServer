import os
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

    def tearDown(self):
        self.app_context.pop()

    '''
    This is a test to make sure that the user cannot view analytics without logging in
    '''
    def test_search_login(self):
        resp = self.client.post('/analytics')
        assert b'You are not logged in' in resp.data

    def test_add_history(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'testing'

        resp = self.client.post('/add-history', data={'id': '1234567'})
        # need to assert that the data is in MongoDB
        assert b'Added article to DB' in resp.data

    def test_analytics_time(self):
        # TODO: after setting up MongoDB code, need to pass dummy data in database
        with self.client.session_transaction() as sess:
            sess['username'] = 'testing'
        resp = self.client.get('/analytics')
        assert b'mins' or b'minutes' in resp.data