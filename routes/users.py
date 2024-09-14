import sqlite3
from flask import render_template, request, jsonify
from . import bp
from database.dbFunctions import get_db


@bp.route('/login')
def login():
    return render_template("login.html")