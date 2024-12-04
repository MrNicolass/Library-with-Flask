import sqlite3
from contextlib import closing
from flask import current_app, g, request

DATABASE = './database/database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('./database/schema.sql', mode='rb') as f:
        db.cursor().executescript(f.read().decode('utf-8'))
    db.commit()

def init_app(app):
    app.teardown_appcontext(close_db)

def records(table : str):
    #Parameters for pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Número de registros por página
    offset = (page - 1) * per_page

    #Connect to the database and fetch the records based on the page and limit
    connection = get_db()
    with closing(connection.cursor()) as cursor:
        #Consult the total number of records
        cursor.execute(f"SELECT COUNT(*) AS total FROM {table}")
        total_records = cursor.fetchone()['total']

        #Consult specific records for the current page
        cursor.execute(f"SELECT * FROM {table} LIMIT {per_page} OFFSET {offset}")
        records = cursor.fetchall()

    connection.close()

    #Calculate the total number of pages
    total_pages = (total_records + per_page - 1) // per_page

    return records, page, total_pages