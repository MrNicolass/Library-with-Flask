from flask import render_template, request, jsonify
from . import bp
from database.dbFunctions import get_db
from flask_dance.contrib.google import google

@bp.route('/')
def first():
    return render_template ("login.html")

@bp.route('/home')
def home():
    google_data = None
    user_info_endpoint = '/oauth2/v2/userinfo'
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()

    return render_template('index.html', google_data=google_data, fetch_url=google.base_url + user_info_endpoint)