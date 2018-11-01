from flask import Flask, request, session, redirect, url_for, render_template
import Article
import requests
import pymongo
import json
from xml.etree import ElementTree
app = Flask(__name__)
app.secret_key = '(*&^!@#*123987'


@app.route('/')
def index():
    if 'username' in session:
        index_articles = db["index_articles"]
        articles = []
        for item in index_articles.find({},{
            "_id": 0,
            'source': 1,
            'title': 1,
            'url': 1,
            'topImage': 1,
            'text': 1,
            'keywords': 1,
            'tags': 1,
            'time': 1
            }):
            articles.append(item)
            hot_word = trending() # hot_word is a list
        return render_template('articles.html', articles=articles, hot_words=hot_word)
    return 'You are not logged in'


@app.route('/search', methods=['POST', 'GET'])
def search():
    if 'username' in session:
        payload = {'q': request.form['keyword'], 'from': '2018-10-20','sortBy': 'publishedAt', 'apiKey': 'eb4ad8625c5b4f57bb62f8c95601038a'}
        r = requests.get('https://newsapi.org/v2/everything', params=payload)
        articles = []
        # TODO: make into Article objects as in update_index()
        # This way, we can also have the time value for articles from search.
        for obj in r.json()['articles']:
            temp = {}
            temp['title'] = obj['title']
            temp['source'] = ''
            temp['url'] = obj['url']
            temp['topImage'] = obj['urlToImage']
            articles.append(temp)
        return render_template('articles.html', articles=articles)
    return 'You are not logged in'


def valid_login():
    user_info = db["user_info"]
    cursor = user_info.find({'username': request.form['username'], 'password': request.form['password']})
    if cursor.count() > 0:
        return True
    return False


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if valid_login():
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return 'Invalid username/password'
    else:
        return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    user_info = db["user_info"]
    if request.method == 'POST':
        if user_info.find({'username': request.form['username']}).count() > 0:
            return 'the username has been used!'
        user_info.insert_one({'username': request.form['username'], 'password': request.form['password']})
        return 'insert success!'
    else:
        return 'use post to signup!'


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


def trending():
    TRENDING_URL = 'http://www.google.com/trends/hottrends/atom/feed?pn=p1'
    r = requests.get(TRENDING_URL)
    root = ElementTree.fromstring(r.content)
    res = []
    for channel in root[0].findall('item'):
        res.append(channel.find('title').text)
    return res


def update_index():
    print('updating main page...')
    payload = {'country': 'US', 'apiKey': 'eb4ad8625c5b4f57bb62f8c95601038a'}
    r = requests.get('https://newsapi.org/v2/top-headlines', params=payload)
    raw_json = r.json()
    index_articles = db["index_articles"]
    index_articles.delete_many({})
    for item in raw_json['articles']:
        article = Article.Article(item['url'])
        article.build()
        index_articles.insert_one({
            'source': article.source_url,
            'title': article.title,
            'url': article.url,
            'topImage':article.top_image,
            'text':article.text,
            'keywords':article.keywords,
            'tags': article.tags,
            'time': article.time
            })
    print('update finished!')

if __name__ == "__main__":
    TRENDING_URL = 'http://www.google.com/trends/hottrends/atom/feed?pn=p1'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    client = pymongo.MongoClient("mongodb+srv://amazon_ec2:1234@cluster0-avowj.mongodb.net/test?retryWrites=true")
    db = client["newsapp"]
    update_index()
    app.run(host="0.0.0.0", port=80)
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    # return render_template('login.html', error=error)
