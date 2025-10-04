import os
import firebase_admin
from firebase_admin import auth as fb_auth, credentials as fb_credentials
import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

# initialize firebase-admin once
_firebase_creds_path = os.getenv('FIREBASE_CREDENTIALS')

if not firebase_admin._apps:
    cred = fb_credentials.Certificate(_firebase_creds_path)
    firebase_admin.initialize_app(cred)

@blueprint.before_app_request
def load_logged_in_user():
    user = session.get('user')
    g.user = user

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', next=request.path))
        return view(*args, **kwargs)
    return wrapped_view

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Client should send a Firebase ID token (e.g. from firebase.auth().currentUser.getIdToken())
    if request.method == 'POST':
        id_token = request.form.get('idToken') or (request.json and request.json.get('idToken'))
        if not id_token:
            flash('Missing idToken', 'error')
            return redirect(url_for('auth.login'))

        try:
            decoded = fb_auth.verify_id_token(id_token)
        except Exception as e:
            flash('Invalid token: {}'.format(e), 'error')
            return redirect(url_for('auth.login'))

        # Save minimal user info in session
        session.clear()
        session['user'] = {
            'uid': decoded.get('uid'),
            'email': decoded.get('email'),
            'firebase_claims': {k: v for k, v in decoded.items() if k not in ('uid','email')}
        }
        return redirect(url_for('index'))

    # GET: render a page that instructs client to sign in via Firebase (or show a JS-based login)
    return render_template('auth/login.html')

@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))