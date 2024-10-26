from flask import render_template, request, jsonify
from . import bp
from database.dbFunctions import get_db
from flask_dance.contrib.google import google
from flask_dance.contrib.github import github

@bp.route('/')
def first():
    return render_template ("login.html")

@bp.route('/home')
def home():
    github_data = None
    git_user_info_endpoint = '/user'

    google_data = None
    google_user_info_endpoint = '/oauth2/v2/userinfo'


    if google.authorized or github.authorized:
        google_data = google.get(google_user_info_endpoint).json()
        github_data = github.get(git_user_info_endpoint).json()
    else:
        return render_template('login.html')

    return render_template('index.html', google_data=google_data, fetch_url=google.base_url + google_user_info_endpoint, github_data=github_data, fetch_url_github=github.base_url + git_user_info_endpoint)