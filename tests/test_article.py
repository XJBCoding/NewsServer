"""
This test checks parsing functionality of the Article class
"""
import requests

import os,sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Article

def init_test():
    """
    This test ensures that an Article object is initialized
    and the url is parsed correctly
    """
    url = 'www.cnn.com/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html'
    article = Article(url)
    assert article
    assert article.source_url == 'www.cnn.com'
    assert article.url == '/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html'

def time_test():
    """ This test ensures that the time estimate is reasonable """
    url = 'www.cnn.com/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html'
    article = Article(url)
    assert article.time > 0 and article.time <= 5

def top_img_test():
    """ This ensures that the top image url exists """
    url = 'www.cnn.com/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html'
    article = Article(url)
    request = requests.get(article.source_url + article.url)
    assert request.status_code == 200
