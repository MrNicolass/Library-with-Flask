from flask import Flask, g, redirect, request, session, url_for
from routes.oAuth import blueprint as google_blueprint
from itsdangerous import URLSafeTimedSerializer
from flask_session import Session
from flask_babel import Babel, gettext as _
from flask_mail import Mail
import json
import os

#Local Imports
from database.dbFunctions import init_app, init_db
from routes.oAuth import github_blueprint
from routes import bp as routes_bp

#Create the Flask app and set configurations
app = Flask(__name__, template_folder= "pages")
app.config["SECRET_KEY"] = "random string"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

#region Functions to handle languages

def read_json_to_tuple(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        #Converte os dados do JSON em uma tupla
        data_tuple = tuple(data.items())
    return data_tuple

def get_locale():
    languages_dict = dict(LANGUAGES)
    return request.cookies.get('language') or request.accept_languages.best_match(languages_dict.keys())

#Define supported languages
json_file_path = os.path.join(os.path.dirname(__file__), './translations/languages.json')
LANGUAGES = read_json_to_tuple(json_file_path)

#endregion

#Initialize app, session, babel and mail
app.session = Session(app)
app.mail = Mail(app)
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)

#region E-mail server configuration

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

#Serializer to generate secure tokens
app.serial = URLSafeTimedSerializer(app.secret_key)

#endregion

#region Blueprints

#Register oAuth Blueprints
app.register_blueprint(google_blueprint, url_prefix="/loginOAuthGoogle")
app.register_blueprint(github_blueprint, url_prefix="/loginOAuthGithub")

#Register routes Blueprint
app.register_blueprint(routes_bp)

#endregion

@app.route('/initdb')
def initialize_db():
    init_db()
    return "<a href='/'>Banco de dados inicializado!</a>"

@app.before_request
def before_request():
    g.locale = get_locale()

@app.route('/set_language', methods=['POST'])
def set_language():
    language = request.form['language'] if 'language' in request.form else 'pt_BR'
    response = redirect(request.referrer) #Redirects to the previous page
    response.set_cookie('language', language)
    session['language'] = language
    return response

#Starts server in debug mode
if __name__ == '__main__':
    app.run(debug=True, port=5000) 