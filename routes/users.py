from flask import render_template, request, jsonify
from . import bp
from database.dbFunctions import get_db
import re
from bcrypt import *

#Funcion if it is a valid email
def email_validation(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

@bp.route('/login')
def login():
    return render_template("login.html")

@bp.route('/register')
def register():
    return render_template("register.html")

@bp.route('/users', methods=['GET', 'POST', 'DELETE'])
def users():
    if request.method == 'GET':
        return get_users()
    elif request.method == 'POST':
        return create_user()
    elif request.method == 'DELETE':
        return block_user()

def get_users():
    try:
        #Database connection handling
        db = get_db()
        cursor = db.cursor()

        #Getting data
        users = cursor.execute("SELECT * FROM users").fetchall()
        #musicas_list = [dict(zip([desc[0] for desc in cursor.description], row)) for row in users]
        return render_template('users.html', dados = users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        db.close()

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
        alreadyExists = cursor.execute(f"SELECT login FROM users WHERE LOWER(login) = LOWER('{login}')").fetchone()

        if alreadyExists:
            return jsonify({"error": "Usuário já existe!"}), 400

        if not email_validation(login):
            return jsonify({"error": "Não é um e-mail Válido!"}), 400

        if not login or not password or not firstName or not lastName:
            return jsonify({"error": "Preencha todos os campos"}), 400
        
        passHash = hashpw(password, gensalt()).decode('utf-8')
        
        cursor.execute(f"INSERT INTO users (login, password, firstName, lastName) VALUES ('{login}', '{passHash}', '{firstName}', '{lastName}')")
        db.commit()
        return jsonify({f"message": "Usuário criado com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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

        #Validation
        userExists = cursor.execute(f"SELECT id FROM users WHERE id = '{id}'").fetchone()
        if not userExists:
            return jsonify({"error": "Usuário não existe!"}), 400

        cursor.execute(f"UPDATE FROM users SET status = 0 WHERE id = '{id}'")
        db.commit()
        return render_template('users.html')

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        db.close()