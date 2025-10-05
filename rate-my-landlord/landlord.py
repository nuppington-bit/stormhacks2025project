import firebase_admin
from firebase_admin import firestore, credentials
import os
import uuid


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

blueprint = Blueprint('landlord', __name__, url_prefix='/landlord')
db = firestore.client()

@blueprint.route('/<landlord_id>', methods=('GET', 'POST'))
def landlord(landlord_id):
    landlord_ref = db.collection('landlord').document(landlord_id)
    landlord = landlord_ref.get()

    reviews_ref = db.collection('review').where("landlordId", '==', landlord_ref)
    reviews = reviews_ref.get()
    
    property_ref = db.collection('property').where("landlordId", '==', landlord_ref)
    properties = property_ref.get()
    review_list = []
    
    for review in reviews:
        review_data = review.to_dict()
        review_data['addressLine1'] = review.get('propertyId').get().get('addressLine1')
        review_list.append(review_data)

    return render_template('landlord.html', landlord_name=landlord.get("name"), landlord=landlord_ref, reviews=review_list, properties=properties)
