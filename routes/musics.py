from flask import make_response, redirect, render_template, request, jsonify, flash, url_for, session
from flask_dance.contrib.google import google
from flask_dance.contrib.github import github
from flask_babel import gettext as _
from . import bp
from database.dbFunctions import get_db, records

#region Musics Functions
@bp.route('/musics', methods=['GET', 'POST'])
def musics():
    if 'session' in session or google.authorized or github.authorized:
        if request.method == 'GET':
            return get_musics()
        
        elif request.method == 'POST':
                return create_music()
    else:
        flash(_("Faça login para acessar essa página!"), "error")
        return redirect(url_for('routes.login'))

@bp.route('/musics/edit/<int:id>', methods=['GET'])
def edit_music(id):
    if 'session' in session or google.authorized or github.authorized:
        cursor = None
        db = None
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM musics WHERE id = ?", (id,))
            music = cursor.fetchone()
            if music:
                return render_template('editMusic.html', dados=music)
            else:
                flash(_("Música não encontrada!"), "error")
                return redirect(url_for('routes.musics'))
        except Exception as e:
            return jsonify({"Error": str(e)}), 500
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    else:
        flash(_("Faça login para acessar essa página!"), "error")
        return redirect(url_for('routes.login'))

def get_musics():
    try:
        # Function to get all musics from database and create pagination
        musics = records('musics')
        return render_template('musics.html', musics=musics[0], page=musics[1], total_pages=musics[2])
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

def create_music():
    cursor = None
    db = None
    try:
        title = request.form['title']
        artist = request.form['artist']
        genre = request.form['genre']

        if not title or not artist or not genre:
            flash(_("Preencha todos os campos"), "error")
            return redirect(url_for('routes.musics'))

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO musics (title, artist, genre) VALUES (?, ?, ?)',
            (title, artist, genre)
        )
        db.commit()
        flash(_("Música cadastrada com sucesso!"), "success")
        return redirect(url_for('routes.musics'))
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()