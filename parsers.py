#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 00:49:13 2018

@author: yuanjihuang
"""
import goose3


class GooseObj(object):
    """encapsulation of goose output"""
    def __init__(self, article):
        g = goose3.Goose({'enable_image_fetching': True})
        goose_obj = g.extract(raw_html=article.html)
        self.body_text = goose_obj.cleaned_text
        keywords = goose_obj.meta_keywords.split(',')
        self.keywords = [w.strip() for w in keywords] # not actual keyw's
        self.title = goose_obj.title
        self.authors = goose_obj.authors
        if goose_obj.top_image:
            self.topImage = goose_obj.top_image.src
        else:
            self.topImage = None
        word_count = len(self.body_text.split())
        self.time = round(word_count/200.0,1)
