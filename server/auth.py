import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

from flask_oauth import OAuth

from flask import redirect

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM admin WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO admin (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
    
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM admin WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.admin = None
    else:
        g.admin = get_db().execute(
            'SELECT * FROM admin WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='eft8S6trlH7Nzj22WWM8a8uYt',
    consumer_secret='qZiipC3Btqyv32eZA3XVef1UZnwegQcEwZlkJc3p3cnjbaDIgT'
)
@twitter.tokengetter
def get_twitter_token(token=None):
    return None
    
@bp.route('/oauth')
def oauth():
    return twitter.authorize(callback=url_for('auth.oauth_authorized',
        next=request.args.get('next') or request.referrer or None))
    
@bp.route('/oauth-authorized')
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
    db.execute(
        'INSERT INTO tokens (username, token, secret) VALUES (?, ?, ?)', (screen_name, oauth_token, oauth_token_secret)
    )
    db.commit()

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(url_for('index'))