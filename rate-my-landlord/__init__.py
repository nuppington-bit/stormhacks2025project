import os
import firebase_admin
from flask import Flask, redirect, render_template, request, session, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    cred = firebase_admin.credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
    firebase_admin.initialize_app(cred)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=('GET', 'POST'))
    def main_page():
        logged_in = 'user_id' in session
        if request.method == 'POST':
            query_term = request.form["query"]
            return redirect(url_for('search.search_results', query=query_term, search="p"))
        return render_template('base.html', logged_in_visibility="hidden" if logged_in else "visible", register="Register" if not logged_in else "Log out", logged_in_url="/auth/logout" if logged_in else "/auth/register")
    
    from . import auth
    from . import review
    from . import search
    from . import landlord

    app.register_blueprint(auth.blueprint)
    app.register_blueprint(review.blueprint)
    app.register_blueprint(search.blueprint)
    app.register_blueprint(landlord.blueprint)

    return app