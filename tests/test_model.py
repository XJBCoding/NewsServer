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
        self.test_model_accuracy()

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
            'http://www.kugn.com/news/model-for-american-girl-doll-reveals-rare-cancer-diagnosis/')
        self.a7.build()

        self.a8 = Article(
            'https://krtv.com/cnn-national/2018/12/02/the-cremated-remains-of-100-people-are-going-to-be-launched-into-space-on-a-spacex-rocket/')
        self.a8.build()

        self.a9 = Article(
            'https://www.cnn.com/2018/12/02/us/elysium-space-memorial-launch/index.html')
        self.a9.build()

        self.a10 = Article(
            'https://www.thesun.ie/news/3466840/emergency-services-race-to-scene-of-crash-involving-several-cars-on-m50-in-dublin/')
        self.a10.build()



    def tearDown(self):
        """called after all test cases finish of this unit"""
        pass

    def test_model_accuracy(self):
        count = 0
        total_test = 10
        
        if self.a1.category == 'entertainment' :
            count += 1
        
        if self.a2.category == 'sports':
            count += 1
        
        if self.a3.category == 'sports':
            count += 1
        
        if self.a4.category == 'technology':
            count += 1
        
        if self.a5.category == 'business':
            count += 1
        
        if self.a6.category == 'technology':
            count += 1

        if self.a7.category == 'health':
            count += 1
        if self.a8.category == 'science':
            count += 1
        if self.a9.category == 'science':
            count += 1

        if self.a10.category == 'general':
            count += 1

        if count/total_test >= 0.8:
            assert True
        