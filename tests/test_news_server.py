import os
import tempfile
from flask import url_for
from news_server import create_app
import pytest
import unittest


class FlaskClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context=self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test(self):
        resp = self.client.post('/login',data = {'username':'123','password':'123'})
        assert resp == 'Invalid username/password'