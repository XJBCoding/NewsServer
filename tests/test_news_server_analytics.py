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
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_add_history(self):
        resp = self.client.post('/add-history', data={'url': 'test', 'mins': 2.3})
        # print(resp.data)
        # need to assert that the data is in MongoDB
        assert True

    def test_analytics_time(self):
        # TODO: after setting up MongoDB code, need to pass dummy data in database
        # yesterday = date.today() - timedelta(1)
        # times.append({'date': yesterday.strftime('%m-%d-%y'), 'mins': 50})
        resp = self.client.get('/analytics')
        assert b'50 minutes' in resp.data