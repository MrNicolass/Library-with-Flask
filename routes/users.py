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

#endregion

#region Users Functions
@bp.route('/users', methods=['GET', 'POST', 'DELETE'])
def users():
    if 'session' in session or google.authorized or github.authorized:
        userId = request.form['id'] if 'id' in request.form else None
        method = request.form['_method'] if '_method' in request.form else None

        if request.method == 'GET':
            return get_users()
        
        elif request.method == 'POST' and (userId == None or userId == "") and method == None:
            return create_user()
        
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
        #Function to get all users from database and create pagination
        users = records('users')
        return render_template('users.html', dados = users[0], page=users[1], total_pages=users[2])

    except Exception as e:
        return jsonify({"Error": str(e)}), 500


def create_user():
    try:
        #Database connection handling
        db = get_db()
        cursor = db.cursor()

        #Getting data
        login = request.form['login']
        password = request.form['password'].encode('utf-8')
        firstName = request.form['firstName']
        lastName = request.form['lastName']

        #Validations
        if userExists(login, cursor):
            return jsonify({"Error": "Usuário já existe!"}), 400

        if not email_validation(login):
            return jsonify({"Error": "Não é um e-mail Válido!"}), 400

        if not login or not password or not firstName or not lastName:
            return jsonify({"Error": "Preencha todos os campos"}), 400
        
        passHash = hashpw(password, gensalt()).decode('utf-8')
        
        cursor.execute(f"INSERT INTO users (login, password, firstName, lastName) VALUES ('{login}', '{passHash}', '{firstName}', '{lastName}')")
        db.commit()
        flash(_("Usuário cadastrado!"), "success")
        return redirect(url_for('routes.login'))

    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    
    finally:
        cursor.close()
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

#endregion