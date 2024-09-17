from flask import render_template, request, jsonify
from . import bp
from database.dbFunctions import get_db
import re

#Funcion if it is a valid email
def email_validation(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(padrao, email):
        return True
    else:
        return False

@bp.route('/login')
def login():
    return render_template("login.html")

@bp.route('/register')
def register():
    return render_template("register.html")

@bp.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        ...
    elif request.method == 'POST':
        return create_user()

def create_user():
    try:
        db = get_db()
        cursor = db.cursor()

        login = request.form['login']
        password = request.form['password']
        firstName = request.form['firstName']
        lastName = request.form['lastName']

        if not email_validation(login):
            return jsonify({"error": "Não é um e-mail Válido!"}), 400

        if not login or not password or not firstName or not lastName:
            return jsonify({"error": "Preencha todos os campos"}), 400
        else:
            cursor.execute(f"INSERT INTO users (login, password, firstName, lastName) VALUES ('{login}', '{password}', '{firstName}', '{lastName}')")
            db.commit()
            return jsonify({"message": "Usuário criado com sucesso!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        db.close()