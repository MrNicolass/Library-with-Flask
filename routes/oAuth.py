from flask import redirect, render_template, request, jsonify, flash, url_for, session, current_app as app
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from itsdangerous import BadSignature, SignatureExpired
from bcrypt import checkpw, gensalt, hashpw
from flask_babel import gettext as _
from dotenv import load_dotenv
from flask_mail import Message
import os

#Local Imports
from routes.users import isUserBlocked, userExists
from database.dbFunctions import get_db
from . import bp

#region Local sets

#Load environment variables
load_dotenv()

#Environment Variables
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Enable http in OAuth
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' # Enable token scope relaxation

#Local Variables
google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

github_client_id = os.getenv("GITHUB_CLIENT_ID")
github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
#endregion

#region Blueprints

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

#endregion

#region OAuth

#Google OAuth
@bp.route('/loginOAuthGoogle')
def loginOAuth():
    if not google.authorized:
        return redirect(url_for("google.login"))
    elif google.authorized:
        google_user_info_endpoint = '/oauth2/v2/userinfo'
        google_data = google.get(google_user_info_endpoint).json()['email']
        email = google_data

        if not userExists(email, get_db().cursor()):
            flash(_("Usuário não cadastrado, cadastre-se primeiro!"), "error")
            session.clear()
            return redirect(url_for("routes.first"))
    else:
        return redirect(url_for("routes.home"))

#Github OAuth
@bp.route('/loginOAuthGithub')
def loginOAuthGithub():
    if not github.authorized:
        return redirect(url_for("github.login"))
    else:
        return redirect(url_for("routes.home"))
    
#endregion

#region Login Functions
@bp.route('/login',  methods=['GET', 'POST'])
def login():
    session['url'] = url_for('routes.login')
    if google.authorized or github.authorized:
        return redirect(url_for('routes.home'))
    elif request.method == 'POST':
        return login_user()
    elif request.method == 'GET':
        return render_template("login.html")
    else:
        return render_template("login.html")

def login_user():
    try:
        #Database connection handling
        db = get_db()
        cursor = db.cursor()

        #Getting data
        login = request.form['login']
        password = request.form['password'].encode('utf-8')

        #Validations
        if not userExists(login, cursor) or isUserBlocked(login, cursor)[0] == 2:
            flash(_("Usuário não cadastrado ou bloqueado, contate o suporte!"), "error")
            return redirect(url_for('routes.login'))
        
        getPassword = cursor.execute(f"SELECT password FROM users WHERE LOWER(login) = LOWER('{login}')").fetchone()[0].encode('utf-8')
        
        if not checkpw(password, getPassword):
            flash(_("Senha Incorreta!"), "error")
            return redirect(url_for('routes.login'))
        else:
            session['session'] = login
            flash(_("Logado com Sucesso!"), "success")
            return redirect(url_for('routes.home'))

        
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        ...

@bp.route('/logout')
def logout():
    session.clear()
    flash(_("Deslogado com Sucesso!"), "success")
    return redirect(url_for('routes.login'))

@bp.route('/register')
def register():
    return render_template("register.html")

@bp.route('/forgotPassword', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        #Prepare the email
        email = request.form['email']
        token = app.serial.dumps(email, salt='password_recovery')
        msg = Message('Recuperação de senha', sender=os.getenv("MAIL_USERNAME"), recipients=[email])

        #check if the e-mail exists
        if not userExists(email, get_db().cursor()):
            flash(_("E-mail não cadastrado."), category='error')
            return render_template("forgotPassword.html")

        #Finish the e-mail body and send it
        link = url_for('routes.forgot_password_user', token=token, _external=True)
        msg.body = f'Clique no link a seguir para redefinir sua senha: {link}'
        app.mail.send(msg)

        flash(_("Um link de recuperação de senha foi enviado para o seu e-mail."), category='success')
        return render_template("forgotPassword.html")
    else:
        return render_template("forgotPassword.html")

@bp.route('/forgotPassword/<token>', methods=['GET', 'POST'])
def forgot_password_user(token):
    try:
        email = app.serial.loads(token, salt='password_recovery', max_age=3600)

    except SignatureExpired:
        flash(_('O link de recuperação de senha expirou.'), category='error')
        return redirect(url_for('forgotPassword'))
    
    except BadSignature:
        flash(_('Link inválido.'), category='error')
        return redirect(url_for('forgotPassword'))

    if request.method == 'POST' and 'password' in request.form:
        new_password = request.form['password'].encode('utf-8')
        passHash = hashpw(new_password, gensalt()).decode('utf-8')

        try:
            #Database connection handling
            db = get_db()
            cursor = db.cursor()
            cursor.execute(f"UPDATE users SET password = '{passHash}', modified = DATETIME(CURRENT_TIMESTAMP, '-3 hours') WHERE login = '{email}'")
            db.commit()

        except Exception as e:
            return jsonify({"Error": str(e)}), 500

        flash(_('Senha alterada com sucesso.'), category='success')
        return redirect(url_for('routes.home'))
    return render_template('recoverPassword.html', token=token)

#endregion