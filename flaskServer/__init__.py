import os
import sqlite3
import functools
import json
import time
from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from .config import *
from .flask_oauth import OAuth

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config)
app.config['SECRET_KEY'] = app.config["SECRET_KEY"]
app.config['DATABASE'] = os.path.join(app.instance_path, 'tokenCollector.sqlite')
     
# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
        
db.init_app(app)
    
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.admin = None
    else:
        g.admin = app.config["ADMIN_NAME"]
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view
    
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/impressum', methods=('GET', 'POST'))
def impressum():
    return render_template('impressum.html')
        
@app.route('/adminView', methods=('GET', 'POST'))
@login_required
def adminView():
    db = get_db()
    tokens = db.execute(
        'SELECT username, token, secret, ts'
        ' FROM tokens'
    ).fetchall()
    dl = []
    for token in tokens:
        dl.append(dict(zip(['username', 'token', 'secret', 'ts'], token)))
    #dl = json.dumps(dl)
    return render_template('adminView.html', tokens=dl, dl=json.dumps(dl))
    
    
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if username != app.config["ADMIN_NAME"]:
            error = 'Incorrect username.'
        elif password != app.config["ADMIN_PW"]:
            error = 'Incorrect password.'

        if error is None:
            session['user_id'] = app.config["ADMIN_NAME"]
            return redirect(url_for('adminView'))

        flash(error)
        
    session.clear()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
        
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view
    
oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=app.config["CONSUMER_KEY"],
    consumer_secret=app.config["CONSUMER_SECRET"]
)
@twitter.tokengetter
def get_twitter_token(token=None):
    return None
        
@app.route('/oauth')
def oauth():
    return twitter.authorize(callback=url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None))
        
@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
        
    screen_name = resp['screen_name']
    oauth_token = resp['oauth_token']
    oauth_token_secret = resp['oauth_token_secret']
           
    db = get_db()
    try:
        db.execute(
            'INSERT INTO tokens (username, token, secret, ts) VALUES (?, ?, ?, ?)', (screen_name, oauth_token, oauth_token_secret, int(time.time()))
        )
        db.commit()
    except sqlite3.Error as er:
        print('er:', er.args)
        
    session['oauth-success'] = screen_name
    flash('API token for %s were saved! Thank you!' % resp['screen_name'])
    return redirect(url_for('index'))
    
if __name__ == "__main__":
    app.run()
