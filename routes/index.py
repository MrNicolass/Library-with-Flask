from flask import flash, redirect, render_template, session, url_for
from flask_dance.contrib.google import google
from flask_dance.contrib.github import github
from flask_babel import gettext as _

from database.dbFunctions import get_db
from routes.users import userExists
from . import bp

@bp.route('/')
def first():
    return render_template("login.html")

@bp.route('/home')
def home():
    # Verifica se há uma sessão ativa (qualquer tipo de login)
    if not ('session' in session or google.authorized or github.authorized):
        flash(_("Faça login para acessar essa página!"), "error")
        return redirect(url_for('routes.login'))

    try:
        db = get_db()
        cursor = db.cursor()
        
        user_name = "Visitante"

        # Define o nome do usuário com base no tipo de login
        if google.authorized:
            google_data = google.get('/oauth2/v2/userinfo').json()
            user_name = google_data.get('name', 'Usuário Google')
        elif github.authorized:
            github_data = github.get('/user').json()
            user_name = github_data.get('name', 'Usuário GitHub')
        elif 'session' in session:
            login_email = session['session']
            user_record = cursor.execute("SELECT firstName FROM users WHERE login = ?", (login_email,)).fetchone()
            if user_record:
                user_name = user_record['firstName']

        # Busca as estatísticas do dashboard
        user_count = cursor.execute("SELECT COUNT(id) FROM users").fetchone()[0]
        music_count = cursor.execute("SELECT COUNT(id) FROM musics").fetchone()[0]

    except Exception as e:
        # Em caso de erro, define valores padrão para evitar que a página quebre
        user_name = "Erro"
        user_count = 0
        music_count = 0
        flash(_("Ocorreu um erro ao carregar os dados do dashboard."), "error")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db' in locals() and db:
            db.close()

    return render_template('index.html', 
                           user_name=user_name, 
                           user_count=user_count, 
                           music_count=music_count)