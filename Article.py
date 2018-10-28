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
        self.top_img = None
        self.text = None
        self.keywords = None
        self.tags = None
        self.is_parsed = False
        self.is_downloaded = False

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
        goose_obj = GooseObj(self)
        self.set_text(goose_obj.body_text)
        self.set_title(goose_obj.title)
        self.set_keywords(goose_obj.keywords)
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
        
    def set_text(self,text):
        self.text = text

    def set_title(self,title):
        self.title = title

    def set_keywords(self,keywords):
        self.keywords = keywords

if __name__ == '__main__':
    a = Article('www.cnn.com/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html')
    a.download()

