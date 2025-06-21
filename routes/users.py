from flask import make_response, redirect, render_template, request, jsonify, flash, url_for, session
from flask_dance.contrib.google import google
from flask_dance.contrib.github import github
from flask_babel import gettext as _
from bcrypt import *
import re
from . import bp
from database.dbFunctions import get_db, records

#region Geral/Validation Functions

#Funcion if it is a valid email
def email_validation(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def userExists(login, cursor):
    return cursor.execute(f"SELECT login FROM users WHERE LOWER(login) = LOWER('{login}')").fetchone()

def isUserBlocked(login, cursor):
    return cursor.execute(f"SELECT status FROM users WHERE LOWER(login) = LOWER('{login}')").fetchone()

def isAdmin(login, cursor):
    return cursor.execute(f"SELECT userType FROM users WHERE LOWER(login) = LOWER('{login}')").fetchone()[0]

#endregion

#region Users Functions
@bp.route('/users', methods=['GET', 'POST', 'DELETE'])
def users():
    
    userId = request.form['id'] if 'id' in request.form else None
    method = request.form['_method'] if '_method' in request.form else None

    if request.method == 'POST' and (userId == None or userId == ""):
        return create_user()

    elif 'session' in session or google.authorized or github.authorized:

        if request.method == 'GET':
            return get_users()
        
        elif request.method == 'POST' and userId != None and method == "DELETE":
            return block_user()
        
        elif request.method == 'POST' and userId != None and method == "GET":
            return get_user()
        
        elif request.method == 'POST' and method == "PUT":
            return edit_user()
    
    else:
        flash(_("Faça login para acessar essa página!"), "error")
        return redirect(url_for('routes.login'))
    
def get_users():
    try:
        db = get_db()
        cursor = db.cursor()

        login_email = None
        # Identifica o e-mail do usuário com base no tipo de sessão
        if 'session' in session:
            login_email = session['session']
        elif google.authorized:
            google_data = google.get('/oauth2/v2/userinfo').json()
            login_email = google_data.get('email')
        elif github.authorized:
            github_data = github.get('/user').json()
            login_email = github_data.get('email')

        # Se não for possível identificar o usuário, redireciona para o login
        if not login_email:
            flash(_("Não foi possível identificar sua sessão. Por favor, faça login novamente."), "error")
            return redirect(url_for('routes.login'))

        # Usa o e-mail unificado para verificar a permissão de administrador
        if not isAdmin(login_email, cursor):
            flash(_("Você não tem permissão para acessar essa página!"), "error")
            return redirect(url_for('routes.home'))
        
        # O resto da função continua como estava, buscando os usuários com paginação
        all_records, page, total_pages = records('users')
        return render_template('users.html', dados=all_records, page=page, total_pages=total_pages)

    except Exception as e:
        # Em vez de retornar um JSON, é melhor redirecionar com uma mensagem de erro
        flash(_("Ocorreu um erro inesperado ao carregar a página de usuários: ") + str(e), "error")
        return redirect(url_for('routes.home'))
    
    finally:
        # Garante que a conexão com o banco seja fechada
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db' in locals() and db:
            db.close()


def create_user():
    try:
        # Conexão com o banco de dados
        db = get_db()
        cursor = db.cursor()

        # Coleta de dados do formulário
        login = request.form['login']
        password = request.form['password'].encode('utf-8')
        firstName = request.form['firstName']
        lastName = request.form['lastName']

        # Validações
        # Verifica se todos os campos foram preenchidos
        if not all([login, password, firstName, lastName]):
            flash(_("Todos os campos são obrigatórios."), "error")
            return redirect(url_for('routes.register'))

        # Verifica se o login é um e-mail válido
        if not email_validation(login):
            flash(_("Por favor, insira um e-mail válido."), "error")
            return redirect(url_for('routes.register'))

        # Verifica se o login já existe
        if userExists(login, cursor):
            flash(_("Este e-mail já está cadastrado. Tente fazer o login."), "error")
            return redirect(url_for('routes.register'))

        # Lógica de Criação e Login Automático
        passHash = hashpw(password, gensalt()).decode('utf-8')
        
        cursor.execute(
            "INSERT INTO users (login, password, firstName, lastName) VALUES (?, ?, ?, ?)",
            (login, passHash, firstName, lastName)
        )
        db.commit()
        
        # Login automático criando a sessão
        session['session'] = login
        
        flash(_("Usuário cadastrado com sucesso! Bem-vindo(a)!"), "success")
        return redirect(url_for('routes.home')) # Redireciona para a página inicial

    except Exception as e:
        # Log do erro seria ideal aqui para depuração
        flash(_("Ocorreu um erro inesperado ao criar o usuário."), "error")
        return redirect(url_for('routes.register'))
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def block_user():
    try:
        #Database connection handling
        db = get_db()
        cursor = db.cursor()

        #Getting data
        id = request.form['id']

        #Validates if user exists
        userExists = cursor.execute(f"SELECT id FROM users WHERE id = '{id}'").fetchone()
        if not userExists:
            flash(_("Usuário não Existe!"), "error")
            return redirect(url_for('routes.users'))
        
        #Verifies if user is already blocked
        if cursor.execute(f"SELECT status FROM users WHERE id = '{id}'").fetchone()[0] == 2:
            flash(_("Usuário já está bloqueado!"), "warning")
            return redirect(url_for('routes.users'))

        cursor.execute(f"UPDATE users SET status = 2, modified = DATETIME(CURRENT_TIMESTAMP, '-3 hours') WHERE id = '{id}'")
        db.commit()
        flash(_("Usuário bloqueado!"), "success")
        return redirect(url_for('routes.users'))

    except Exception as e:
        flash(_(f"Erro: {str(e)}"), "error")
        return redirect(url_for('routes.users'))
    
    finally:
        cursor.close()
        db.close()

def get_user():
    try:
        #Database connection handling
        db = get_db()
        cursor = db.cursor()

        #Getting data and exhibiting it
        id = request.form['id']
        getUser = cursor.execute(f"SELECT * FROM users WHERE id = '{id}'").fetchone()
        return render_template('editUser.html', dados = getUser, usuario = (f"{getUser[3]} {getUser[4]}"))

    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    
    finally:
        cursor.close()
        db.close()

def edit_user():
    try:
        #Database connection handling
        db = get_db()
        cursor = db.cursor()

        #Getting data
        id = request.form['id']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        status = request.form['optionsStatus']

        #Validations
        if not firstName or not lastName or not status:
            return jsonify({"Error": "Preencha todos os campos"}), 400
        
        cursor.execute(f"UPDATE users SET firstName = '{firstName}', lastName = '{lastName}', status = '{status}', modified = DATETIME(CURRENT_TIMESTAMP, '-3 hours') WHERE id = '{id}'")
        db.commit()
        flash(_("Usuário editado!"), "success")
        return redirect(url_for('routes.users'))

    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@bp.route('/profile')
def profile():
    # 1. Proteção da rota: verifica se o usuário está logado
    if not ('session' in session or google.authorized or github.authorized):
        flash(_("Faça login para acessar essa página!"), "error")
        return redirect(url_for('routes.login'))

    login_email = None
    try:
        # 2. Identifica o e-mail do usuário com base no tipo de sessão
        if 'session' in session:
            login_email = session['session']
        elif google.authorized:
            google_data = google.get('/oauth2/v2/userinfo').json()
            login_email = google_data.get('email')
        elif github.authorized:
            github_data = github.get('/user').json()
            login_email = github_data.get('email')
        
        if not login_email:
            flash(_("Não foi possível identificar seu usuário. Por favor, faça login novamente."), "error")
            return redirect(url_for('routes.logout'))

        # 3. Busca os dados completos do usuário no banco de dados
        db = get_db()
        cursor = db.cursor()
        user_data = cursor.execute("SELECT * FROM users WHERE login = ?", (login_email,)).fetchone()

        if not user_data:
            # Caso o usuário logado via OAuth não exista no banco local
            flash(_("Seu usuário não foi encontrado em nosso sistema."), "error")
            return redirect(url_for('routes.logout'))

        # 4. Renderiza a página de perfil com os dados do usuário
        return render_template('profile.html', user_data=user_data)

    except Exception as e:
        flash(_("Ocorreu um erro ao carregar seu perfil. Detalhes: ") + str(e), "error")
        return redirect(url_for('routes.home'))
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db' in locals() and db:
            db.close()

@bp.route('/profile/change-password', methods=['POST'])
def change_password():
    # 1. Proteção da rota e identificação do usuário
    if not ('session' in session or google.authorized or github.authorized):
        flash(_("Faça login para acessar essa página!"), "error")
        return redirect(url_for('routes.login'))

    # Identifica o e-mail do usuário a partir da sessão (apenas usuários internos podem trocar a senha aqui)
    if 'session' not in session:
        flash(_("Usuários logados com Google ou GitHub não podem alterar a senha por aqui."), "error")
        return redirect(url_for('routes.profile'))
    
    login_email = session['session']

    # 2. Coleta de dados do formulário
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # 3. Validações
    if not all([current_password, new_password, confirm_password]):
        flash(_("Todos os campos de senha são obrigatórios."), "error")
        return redirect(url_for('routes.profile'))

    if new_password != confirm_password:
        flash(_("A nova senha e a confirmação não correspondem."), "error")
        return redirect(url_for('routes.profile'))

    db = get_db()
    cursor = db.cursor()
    try:
        user_data = cursor.execute("SELECT password FROM users WHERE login = ?", (login_email,)).fetchone()

        # Validação de segurança: verifica se a senha atual está correta
        stored_hash = user_data['password'].encode('utf-8')
        if not checkpw(current_password.encode('utf-8'), stored_hash):
            flash(_("A senha atual está incorreta."), "error")
            return redirect(url_for('routes.profile'))

        # 4. Atualização da senha no banco de dados
        new_hash = hashpw(new_password.encode('utf-8'), gensalt()).decode('utf-8')
        
        # Usando a data/hora local correta de acordo com a documentação do projeto
        cursor.execute("UPDATE users SET password = ?, modified = DATETIME('now', '-3 hours') WHERE login = ?", (new_hash, login_email))
        db.commit()

        flash(_("Senha alterada com sucesso!"), "success")

    except Exception as e:
        flash(_("Ocorreu um erro ao alterar a senha: ") + str(e), "error")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('routes.profile'))

#endregion