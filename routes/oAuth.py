from flask import redirect, render_template, request, jsonify, flash, url_for
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
import re
import os

#Load environment variables
load_dotenv()

#Local Imports
from . import bp
from database.dbFunctions import get_db

#Environment Variables
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Enable http in OAuth
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' # Enable token scope relaxation

google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")

#Google Blueprint
blueprint = make_google_blueprint(
    client_id=google_client_id,
    client_secret=google_client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)

#Github Blueprint
github_blueprint = make_github_blueprint(
    client_id=github_client_id,
    client_secret=github_client_secret,
    scope="user:email"
)

@bp.route('/loginOAuthGoogle')
def loginOAuth():
    if not google.authorized:
        return redirect(url_for("google.login"))
    else:
        return redirect(url_for("routes.home"))
    
#region Github OAuth

@bp.route('/loginOAuthGithub')
def loginOAuthGithub():
    if not github.authorized:
        return redirect(url_for("github.login"))
    else:
        return redirect(url_for("routes.home"))
    
#endregion