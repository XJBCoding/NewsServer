from flask import Flask,render_template,request
app = Flask(__name__)
'''
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
'''


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        return request.form['username']
    else:
        return 'fuck'


'''with app.test_request_context('/hello', method='GET'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:

    assert request.path == '/hello'
    assert request.method == 'GET'
    print(request.form['username'])'''