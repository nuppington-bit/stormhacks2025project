import firebase_admin
from firebase_admin import firestore, credentials
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

blueprint = Blueprint('auth', __name__, url_prefix='/auth')
cred = firebase_admin.credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
firebase_admin.initialize_app(cred)
db = firestore.client()
@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        emailAddress = request.form['emailAddress']
        password = request.form['password']
        existing_user = db.collection('user').where('emailAddress', '==', emailAddress).get()
        error = None
        if existing_user:
            error = f"User {emailAddress} is already registered."
            return redirect(url_for('auth.login'))
        if not emailAddress:
            error = 'emailAddress is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            db.collection('user').add({
                'emailAddress': emailAddress,
                'password': generate_password_hash(password)
            })
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        emailAddress = request.form['emailAddress']
        password = request.form['password']
        error = None
        user = db.collection('user').where('emailAddress', '==', emailAddress).get()

        if not user:
            error = 'Incorrect emailAddress.'
        elif not check_password_hash(user[0].get('password'), password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0].id
            return redirect("/")

        flash(error)

    return render_template('auth/login.html')