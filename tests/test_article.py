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


class ArticleTestCase(unittest.TestCase):

    def setUp(self):
        """called before the first test case of this unit begins"""
        self.article = Article(
            'www.cnn.com/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html')
        
        self.invalid_article = Article(
            'i am an invalid string')

    def tearDown(self):
        """called after all test cases finish of this unit"""
        pass

    def test_url(self):
        assert self.article.url == '/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html'

    def test_source_url(self):
        assert self.article.source_url == 'http://www.cnn.com'
        request = requests.get(self.article.source_url + self.article.url)
        assert request.status_code == 200

    def test_download_html(self):
        self.article.download()

        assert len(self.article.html) > 5000

    def test_parse_html_valid(self):
        """check whether parser function can use GooseObj correctly"""
        TOP_IMG = 'https://cdn.cnn.com/cnnnext/dam/assets/180925092633-03-iyw-wisniewski-trnds-large-169.jpg'
        TITLE = "4-year-old Florence didn't like sharing her name with a bad hurricane. So she did something about it."
        KEYWORDS = ['health', "4-year-old Florence didn't like sharing her name with a bad hurricane. So she did something about it. - CNN"]
        self.article.download()
        self.article.parse()
        assert self.article.topImage == TOP_IMG
        assert self.article.title == TITLE
        assert self.article.keywords == KEYWORDS

    def test_time_valid(self):
        self.article.download()
        self.article.parse()
        assert self.article.time == 2.5

    def test_url_invalid(self):
        self.invalid_article.download()
        self.assertRaises(Exception, self.invalid_article.parse())

    def test_url_empty(self):
        self.assertRaises(Exception, Article, '')
