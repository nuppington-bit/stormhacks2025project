import firebase_admin
from firebase_admin import firestore, credentials
import os
import uuid


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

blueprint = Blueprint('search', __name__, url_prefix='/search')
db = firestore.client()

@blueprint.route('/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        query_term = request.form["query"]
        query = db.collection("landlord" if request.args.get("search") == "l" else "property").where("name", ">=", query_term).where("name", "<", query_term + "\uf8ff")
        data = query.get()
        
        return render_template('search.html', label="landlords" if request.args.get("search") == "l" else "properties", data=data, offset=1)
        # return redirect("/")
    return render_template('search.html', label="landlords" if request.args.get("search") == "l" else "properties", offset=1)
