from flask import Flask, request, session, redirect, url_for, render_template
from Article import Article
import requests
import pymongo
from xml.etree import ElementTree
from datetime import date, timedelta
import threading
import atexit

articles = []

POOL_TIME = 120 #Seconds

# variables that are accessible from anywhere
commonDataStruct = {}
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
refreshThread = threading.Thread()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='sd*&^!@#*123987')
    client = pymongo.MongoClient("mongodb+srv://news:123@cluster0-avowj.mongodb.net/test?retryWrites=true")
    db = client["newsapp"]
    # Refresh main page when starting server, use this code
    update_index(db)

    def interrupt():
        global refreshThread
        refreshThread.cancel()

    def doStuff():
        global commonDataStruct
        global refreshThread
        with dataLock:
        # Do your stuff with commonDataStruct Here
            update_index(db)
        # Set the next thread to happen
        refreshThread = threading.Timer(POOL_TIME, doStuff, ())
        refreshThread.start()

    def doStuffStart():
        # Do initialisation stuff here
        global refreshThread
        # Create your thread
        refreshThread = threading.Timer(POOL_TIME, doStuff, ())
        refreshThread.start()

    # Refresh main page periodically, use this code
    #doStuffStart()
    #atexit.register(interrupt)




    @app.route('/')
    def index():
        if 'username' in session:
            index_articles = db["articles"]
            articles = []
            for item in index_articles.find({'is_index': 1}, {
                "_id": 1,
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
                hot_word = trending() # hot_word is a dictionary, element:{word: weight}
            return render_template('articles.html', articles=articles, hot_words=hot_word.keys())
        return render_template('login.html')

    @app.route('/search', methods=['POST', 'GET'])
    def search():
        if 'username' in session:
            if (request.form['keyword'] == None or request.form['keyword'] == '') and (request.form['sources'] == None or request.form['sources'] == ''):
                return redirect(url_for('index'))
            payload = {'q': request.form['keyword'], 'sources': request.form['sources'],'language':'en','from': '2018-11-25','sortBy': 'relevancy', 'apiKey': 'eb4ad8625c5b4f57bb62f8c95601038a'}
            r = requests.get('https://newsapi.org/v2/everything', params=payload)
            raw_json = r.json()
            index_articles = db["articles"]
            index_articles.delete_many({'is_index': 1})
            for item in raw_json['articles']:
                article = Article(item['url'])
                article.build()
                index_articles.insert_one({
                    'source': article.source_url,
                    'title': article.title,
                    'url': article.url,
                    'topImage': article.top_image,
                    'text': article.text,
                    'keywords': article.keywords,
                    'tags': article.tags,
                    'category': article.category,
                    'time': article.time,
                    'is_index': 1
                })






            articles = []
            # TODO: make into Article objects as in update_index()
            # This way, we can also have the time value for articles from search.
            for obj in r.json()['articles']:
                temp = {}
                temp['title'] = obj['title']
                temp['source'] = ''
                temp['url'] = obj['url']
                temp['topImage'] = obj['urlToImage']
                temp['text'] = obj['content']
                articles.append(temp)
            return render_template('articles.html', articles=articles)
        return 'You are not logged in'

    @app.route('/add-history', methods=['POST'])
    def add_history():
        if 'username' in session:
            user_history = db["user_history"]
            time = {'username': session['username'],'article_id':request.form['id'],'date':date.today().strftime('%m-%d-%y')}
            user_history.insert_one(time)
        return 'You are not logged in'

    @app.route('/analytics')
    def analytics():
        user_history = db["user_history"]
        index_articles = db["user_history"]
        times = []
        #for items in user_history.find({'username':session['username']}):



        times.append({'date': date.today().strftime('%m-%d-%y'), 'mins': 40})
        yesterday = date.today() - timedelta(1)
        times.append({'date': yesterday.strftime('%m-%d-%y'), 'mins': 50})
        # return render_template('analytics.html')
        return render_template('analytics.html', times=times)

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if request.method == 'POST':
            if valid_login(db):
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

    return app


def valid_login(db):
    user_info = db["user_info"]
    cursor = user_info.find({'username': request.form['username'], 'password': request.form['password']})
    if cursor.count() > 0:
        return True
    return False


def trending():
    TRENDING_URL = 'http://www.google.com/trends/hottrends/atom/feed?pn=p1'
    r = requests.get(TRENDING_URL)
    root = ElementTree.fromstring(r.content)
    res = {}
    for channel in root[0].findall('item'):
        weight=100
    #     tem = channel.find('{https://trends.google.com/trends/hottrends}approx_traffic').text.split('+')[0]
    #     tem = tem.split(',')
    #     weight = ''
    #     for i in tem:
    #         weight += i
        res[channel.find('title').text] = int(weight)
    return res


def update_index(db):
    print('updating main page...')
    payload = {'country': 'US', 'apiKey': 'eb4ad8625c5b4f57bb62f8c95601038a'}
    r = requests.get('https://newsapi.org/v2/top-headlines', params=payload)
    raw_json = r.json()
    index_articles = db["articles"]
    index_articles.delete_many({'is_index': 1})
    for item in raw_json['articles']:
        article = Article(item['url'])
        article.build()
        index_articles.insert_one({
            'source': article.source_url,
            'title': article.title,
            'url': article.url,
            'topImage':article.top_image,
            'text':article.text,
            'keywords':article.keywords,
            'tags': article.tags,
            'category': article.category,
            'time': article.time,
            'is_index': 1
            })
    print('update finished!')

# the code below is executed if the request method
# was GET or the credentials were invalid
# return render_template('login.html', error=error)


if __name__ == '__main__':
    app = create_app()
    app.run()