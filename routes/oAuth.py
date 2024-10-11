from flask import redirect, render_template, request, jsonify, flash, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from main import app
import re
import os

#Local Imports
from . import bp
from database.dbFunctions import get_db

#Environment Variables
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #Enable http in OAuth
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' #Enable token scope relaxation

#Local Variables
client_id = "631204901975-2g4mjp5scd4jmd9lbl8ck3p9qpmhquoi.apps.googleusercontent.com"
client_secret = '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'
app.secret_key = 'makolindoMonstro'

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)

app.register_blueprint(blueprint, url_prefix="/loginOAuth")

@bp.route('/loginOAuth')
def loginOAuth():
    if not google.authorized:
        return redirect(url_for("google.login"))