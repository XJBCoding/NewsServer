from flask import Flask,url_for
app = Flask(__name__)


@app.route('/')
def index():
    return 'helloworld!'


'''
string  accepts any text without a slash
int	    accepts positive integers
float	accepts positive floating point values
path	like string but also accepts slashes
uuid	accepts UUID strings

'''


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath


'''
The canonical URL for the projects endpoint has a trailing slash. 
It’s similar to a folder in a file system. If you access the URL 
without a trailing slash, Flask redirects you to the canonical URL
with the trailing slash.

The canonical URL for the about endpoint does not have a trailing 
slash. It’s similar to the pathname of a file. Accessing the URL 
with a trailing slash produces a 404 “Not Found” error. This helps 
keep URLs unique for these resources, which helps search engines 
avoid indexing the same page twice.
'''


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


@app.route('/login')
def login():
    return 'login'


@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))