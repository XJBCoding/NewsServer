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
        self.a1 = Article(
            'https://www.eonline.com/news/992346/nick-jonas-and-priyanka-chopra-s-wedding-may-be-the-most-over-the-top-of-them-all')
        self.a1.build()
        self.a2 = Article(
            'https://www.cbssports.com/college-football/news/college-football-picks-schedule-predictions-for-major-2018-conference-championship-games-today/')
        self.a2.build()
        self.a3 = Article(
            'https://www.ksl.com/article/46438688/the-triple-option-utahs-defense-gives-enough-but-offense-sputters')
        self.a3.build()
        self.a4 = Article(
            'https://carbuzz.com/news/this-is-when-the-porsche-911-hybrid-is-likely-to-arrive')
        self.a4.build()
        self.a5 = Article(
            'https://www.reuters.com/article/us-g20-argentina/trump-chinas-xi-poised-for-high-stakes-summit-over-trade-war-idUSKCN1O031C')
        self.a5.build()
        self.a6 = Article(
            'https://www.engadget.com/2018/12/01/amazon-music-android-tv/')
        self.a6.build()
        self.a7 = Article(
            'https://www.thetimes.co.uk/article/nasa-probe-closes-in-on-asteroid-in-hunt-for-first-sample-2jx3mbx7x')
        self.a7.build()
        
        self.a8 = Article(
            'https://www.aljazeera.com/news/2018/12/china-declare-trade-war-ceasefire-trump-xi-summit-181202031620261.html')
        self.a8.build()

        self.a9 = Article(
            'https://www.dailymail.co.uk/news/article-6451239/You-lean-s-t-doesnt-work-Michelle-Obama-shocks-audience.html')
        self.a9.build()

        self.a10 = Article(
            'https://www.theverge.com/2018/11/29/18116830/crispr-baby-he-jiankui-genetics-ethics-science-health-mutation')
        self.a10.build()

    def tearDown(self):
        """called after all test cases finish of this unit"""
        pass

    def test_case1(self):
        assert self.a1.category == 'entertainment' 
    def test_case2(self):
        assert self.a2.category == 'sports' 
    def test_case3(self):
        assert self.a3.category == 'sports' 
    def test_case4(self):
        assert self.a4.category == 'technology' 
    def test_case5(self):
        assert self.a5.category == 'business' 
    def test_case6(self):
        assert self.a6.category == 'technology' 
    def test_case7(self):
        assert self.a7.category == 'technology'

    def test_case8(self):
        assert self.a8.category == 'business'
    def test_case9(self):
        assert self.a9.category == 'entertainment' 
    def test_case10(self):
        assert self.a10.category == 'health'
        