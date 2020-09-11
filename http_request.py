from flask import Flask, request
from markupsafe import escape


app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
def show_the_login_form():
    return 'User %s' % escape(request.method)
def do_the_login():
    return 'this is the log in'

