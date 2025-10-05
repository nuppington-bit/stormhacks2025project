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


@blueprint.route('/submit/<landlord_id>/<property_id>', methods=('GET', 'POST'))
def submit_review(landlord_id, property_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    if request.method == 'POST':
        rating = request.form['rating']
        body = request.form['body']
        landlord_id = db._get_collection_reference(
            'landlord').document(landlord_id)
        property_id = db._get_collection_reference(
            'property').document(property_id)
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
