from itsdangerous import URLSafeTimedSerializer
from routes.oAuth import blueprint as google_blueprint
from database.dbFunctions import init_app, init_db
from routes.oAuth import github_blueprint
from flask_session import Session
from flask_mail import Mail
from flask import Flask
import os

#Local Imports
from routes import bp as routes_bp

app = Flask(__name__, template_folder= "pages")
app.config["SECRET_KEY"] = "random string"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.session = Session(app)

#Initialize the database
init_app(app)

#region E-mail server configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.mail = Mail(app)

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

#Starts server in debug mode
if __name__ == '__main__':
    app.run(debug=True, port=5000) 