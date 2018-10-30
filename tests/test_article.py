"""
This test checks parsing functionality of the Article class
"""
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import requests
import Article

def test_init():
    """
    This test ensures that an Article object is initialized
    and the url is parsed correctly
    """
    url = 'www.cnn.com/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html'
    article = Article.Article(url)
    assert article
    assert article.source_url == 'http://www.cnn.com'
    assert article.url == '/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html'

def test_time():
    """ This test ensures that the time estimate is reasonable """
    url = 'www.cnn.com/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html'
    article = Article.Article(url)
    article.build()
    assert article.time
    assert article.time > 0 and article.time <= 5

def test_top_img():
    """ This ensures that the top image url exists """
    url = 'www.cnn.com/2018/09/25/health/iyw-girl-named-florence-collects-donations-trnd/index.html'
    article = Article.Article(url)
    article.build()
    request = requests.get(article.source_url + article.url)
    assert request.status_code == 200
