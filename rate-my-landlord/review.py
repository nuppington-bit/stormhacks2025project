import firebase_admin
from firebase_admin import firestore, credentials
import os
import uuid


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

blueprint = Blueprint('review', __name__, url_prefix='/review')
db = firestore.client()

@blueprint.route('/', methods=('GET', 'POST'))
@blueprint.route('/submit/', methods=('GET', 'POST'))
def submit_review():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    if request.method == 'POST':
        rating = request.form['rating']
        body = request.form['body']
        landlord_id = request.form['landlord_id']
        property_id = request.form['property_id']
        title = request.form['title']
        db.collection('review').add({
            'title': title,
            'rating': rating,
            'body': body,
            'userId': db._get_collection_reference('user').document(session['user_id']),
            'landlordId': landlord_id,
            'propertyId': property_id
        })
        return redirect("/")
    return render_template('review.html')
