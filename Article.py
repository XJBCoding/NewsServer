#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 00:49:13 2018

@author: yuanjihuang
"""
import sys
import pymongo
from urllib.parse import urlparse
import requests
from parsers import GooseObj
from models import transform, predict
import numpy as np

class Article(object):

    def __init__(self, url, source_url = ''):
        if source_url == '':
            parsed_url = urlparse(url)
            scheme = parsed_url.scheme
            if scheme is '':
                scheme = 'http'
                parsed_url = urlparse(scheme + '://' + url)
            source_url = scheme + '://' + parsed_url.netloc
            url = parsed_url.path
            print(parsed_url)
            if parsed_url.netloc == '':
                raise Exception('input do not have source!')
        self.url = url
        self.html = None
        self.source_url = source_url
        self.top_image = None
        self.text = None
        self.keywords = None
        self.tags = None
        self.time = None
        self.author = None
        self.is_parsed = False
        self.is_downloaded = False
        self.category = None

        self.model = np.load('model.npy').item()
        self.mapping = np.load('dictionary.npy').item()

    def build(self):
        # Build a lone article from a URL independent of the source (newspaper).
        self.download()
        self.parse()
        self.nlp()

    def download(self):
        print(self.source_url + self.url)
        self.html = self.get_html(self.source_url + self.url)
        self.is_downloaded = True

    def parse(self):
        if self.is_downloaded is False:
            raise Exception('You should download first!')
        try:
            goose_obj = GooseObj(self)
        except:
            print ('[REQUEST FAILED]')
            return u''
        self.set_text(goose_obj.body_text)
        self.set_title(goose_obj.title)
        self.set_keywords(goose_obj.keywords)
        if goose_obj.top_image:
            self.set_top_image(goose_obj.top_image)
        self.set_time(goose_obj.time)
        self.set_authors(goose_obj.authors)
        self.is_parsed = True

    def get_html(self,url):
        # retrieves the html for either a url or a response object
        try:
            html = requests.get(url=url).text
            if html is None:
                html = ''
            return html
        except:
            print ('[REQUEST FAILED]')
            return u''

    def nlp(self):
        # keyword extraction wrapper
        if not self.is_downloaded or not self.is_parsed:
            raise Exception('You should download and parse first!')
        #Todo
        tem = transform(self.text, self.mapping)
        result = predict(self.model, tem)
        self.set_category(result[0])

    def set_category(self, cat):
        mapping_list = ['technology','business','entertainment','general','sports','health','science']
        self.category = mapping_list[cat-1]

    def set_text(self,text):
        self.text = text

    def set_title(self,title):
        self.title = title

    def set_keywords(self,keywords):
        self.keywords = keywords

    def set_top_image(self,top_image):
        self.top_image = top_image

    def set_authors(self,author):
        self.author = author

    def set_time(self,time):
        self.time = time

'''if __name__ == '__main__':
    a = Article('www.cnn.com/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html')
    a.build()
    print('url:', a.url)
    print('source_url:', a.source_url)
    print('TOP_IMG:', a.top_img)
    print('text:', a.text)
    print('title:', a.title)
    print('keywords:', a.keywords)
    print('time:', a.time)
    print('author:', a.author)'''

