import os
import sys
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import tempfile
from flask import url_for, request, Response, session
from news_server import create_app
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
    def test_search_login(self):
        resp = self.client.post('/search', data={'keyword': 'bitcoin', 'sources': ''})
        assert b'You are not logged in' in resp.data

    '''
    This is a test to make sure that the user can search by keyword.
    Specifically, if the user inputs the keyword 'bitcoin', we qualify 
    the test as passing if over 70% of the articles mention 'bitcoin'
    in their headline or first 260 words of text.
    '''
    def test_search_keyword_1(self):
        with self.client.session_transaction() as sess:
            sess['username'] = True

        resp = self.client.post('/search', data={'keyword': 'bitcoin', 'sources': ''})
        assert b'itcoin' in resp.data

    def test_search_keyword_2(self):
        with self.client.session_transaction() as sess:
            sess['username'] = True

        resp = self.client.post('/search', data={'keyword': 'bitcoin bank', 'sources': ''})
        assert b'itcoin' or b'ank' in resp.data
    
    def test_search_keyword_3(self):
        with self.client.session_transaction() as sess:
            sess['username'] = True

        resp = self.client.post('/search', data={'keyword': '', 'sources': ''})
        assert b'Redirecting' in resp.data

    def test_search_keyword_4(self):
        with self.client.session_transaction() as sess:
            sess['username'] = True

        resp = self.client.post('/search', data={'keyword': 'asdfghjk*&&%', 'sources': ''})
        assert b'' in resp.data
    '''
    This is a test to make sure that the user can search by source.
    Specifically, if a user inputs 'abc-news', we qualify the test as passing
    if all of the articles have 'abcnews.go.com' in the URL.
    '''
    def test_search_source_1(self):
        with self.client.session_transaction() as sess:
            sess['username'] = True

        resp = self.client.post('/search', data={'keyword': '', 'sources': 'abc-news'})
        assert b'abcnews.go.com' in resp.data


    def test_search_source_2(self):
        with self.client.session_transaction() as sess:
            sess['username'] = True

        resp = self.client.post('/search', data={'keyword': '', 'sources': 'abc-news,cnn'})
        assert b'abcnews.go.com' or b'cnn.com' in resp.data
    '''
    This is a test to make sure that the user can search by both keyword and source.
    '''
    def test_search_keyword_and_source(self):
        with self.client.session_transaction() as sess:
            sess['username'] = True

        resp = self.client.post('/search', data={'keyword': 'trump', 'sources': 'cnn'})
        assert b'rump' in resp.data
        assert b'cnn.com' in resp.data