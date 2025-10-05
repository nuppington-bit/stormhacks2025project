import firebase_admin
from firebase_admin import firestore
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

blueprint = Blueprint('search', __name__, url_prefix='/search')
db = firestore.client()


@blueprint.route('/', methods=('GET', 'POST'))
def search():
    query_term = request.args.get('query') or request.form.get('query', '')

    if not query_term:
        # No query entered, just render empty search page
        return render_template(
            'search.html',
            label="landlords" if request.args.get(
                "search") == "l" else "properties",
            data=[],
            offset=0
        )

    # Determine if searching landlords or properties
    search_type = request.args.get("search", "l")  # default to landlords

    if search_type == "l":
        # Firestore query for landlord name
        query = db.collection("landlord").where(
            "name", ">=", query_term).where("name", "<=", query_term + "\uf8ff")
    else:
        # Firestore query for property address
        query = db.collection("property").where(
            "addressLine1", ">=", query_term).where("addressLine1", "<=", query_term + "\uf8ff")

    data = query.get()

    # If exactly one landlord is found, redirect to their page
    if search_type == "l" and len(data) == 1:
        landlord_id = data[0].id
        return redirect(url_for('landlord.landlord', landlord_id=landlord_id))

    return render_template(
        'search.html',
        label="landlords" if search_type == "l" else "properties",
        data=data,
        offset=0
    )
