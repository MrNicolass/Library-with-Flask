from flask_dance.contrib.google import google
from flask_dance.contrib.github import github

from flask import flash, redirect, render_template, session, url_for
from database.dbFunctions import get_db
from routes.users import userExists
from . import bp

@bp.route('/')
def first():
    return render_template ("login.html")

@bp.route('/home')
def home():
    github_data = None
    git_user_info_endpoint = '/user'

    google_data = None
    google_user_info_endpoint = '/oauth2/v2/userinfo'

    sessao = session['session'] if 'session' in session else None

    if google.authorized:
        google_data = google.get(google_user_info_endpoint).json()
        email =google_data['email']

        if not userExists(email, get_db().cursor()):
            session.clear()
            flash("Usuário não cadastrado, cadastre-se primeiro!", "error")
            return redirect(url_for("routes.first"))
        
    elif github.authorized:
        github_data = github.get(git_user_info_endpoint).json()

    elif 'session' in session:
        return render_template('index.html', google_data=google_data, fetch_url=google.base_url + google_user_info_endpoint, github_data=github_data, session=sessao, fetch_url_github=github.base_url + git_user_info_endpoint)
    
    else:
        flash("Faça login para acessar essa página!", "error")
        return redirect(url_for('routes.login'))

    return render_template('index.html', google_data=google_data, fetch_url=google.base_url + google_user_info_endpoint, github_data=github_data, session=sessao, fetch_url_github=github.base_url + git_user_info_endpoint)