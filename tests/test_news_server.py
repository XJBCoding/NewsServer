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


class FlaskClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_login1(self):
        "If username and password are all empty"
        resp = self.client.post('/login', data={'username': '', 'password': ''})
        assert b'Invalid username/password' in resp.data

    def test_login2(self):
        "If username is correct but password is  empty"
        resp = self.client.post('/login', data={'username': 'huang1234', 'password': ''})
        assert b'Invalid username/password' in resp.data

    def test_login3(self):
        "If username is empty but password is correct"
        resp = self.client.post('/login', data={'username': '', 'password': '123'})
        assert b'Invalid username/password' in resp.data

    def test_login4(self):
        "If username and password are not match"
        resp = self.client.post('/login', data={'username': 'huang1234', 'password': '123456'})
        assert b'Invalid username/password' in resp.data

    def test_login5(self):
        "If username and password are correct and match"
        resp = self.client.post('/login', data={'username': 'huang1234', 'password': '123'})
        # print(resp.data)
        assert b'Invalid username/password' not in resp.data
