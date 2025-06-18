from flask import redirect, render_template, request, flash, url_for, session
from flask_babel import gettext as _
from . import bp
from database.dbFunctions import get_db, records

# ROTA PARA LISTAR AS MÚSICAS (AGORA SOMENTE GET)
@bp.route('/musics', methods=['GET'])
def musics():
    # Proteção da rota
    if not ('session' in session or 'google' in session or 'github' in session):
        flash(_("Faça login para acessar essa página!"), "error")
        return redirect(url_for('routes.login'))
    
    try:
        # Busca os registros com paginação
        all_records, page, total_pages = records('musics')
        return render_template('musics.html', musics=all_records, page=page, total_pages=total_pages)
    except Exception as e:
        flash(_("Ocorreu um erro ao carregar as músicas: ") + str(e), "error")
        # Retorna uma página vazia em caso de erro para não quebrar a aplicação
        return render_template('musics.html', musics=[], page=1, total_pages=1)

# NOVA ROTA PARA ADICIONAR MÚSICAS
@bp.route('/musics/add', methods=['GET', 'POST'])
def add_music():
    # Proteção da rota
    if not ('session' in session or 'google' in session or 'github' in session):
        flash(_("Faça login para acessar essa página!"), "error")
        return redirect(url_for('routes.login'))

    # Se a requisição for POST, processa o formulário
    if request.method == 'POST':
        db = None
        cursor = None
        try:
            title = request.form['title']
            artist = request.form['artist']
            genre = request.form['genre']

            # Validação simples
            if not all([title, artist, genre]):
                flash(_("Todos os campos são obrigatórios."), "error")
                return redirect(url_for('routes.add_music'))

            db = get_db()
            cursor = db.cursor()
            
            # Query parametrizada para evitar SQL Injection
            cursor.execute(
                'INSERT INTO musics (title, artist, genre) VALUES (?, ?, ?)',
                (title, artist, genre)
            )
            db.commit()
            
            flash(_("Música cadastrada com sucesso!"), "success")
            return redirect(url_for('routes.musics')) # Redireciona para a lista após o sucesso
        
        except Exception as e:
            flash(_("Ocorreu um erro ao cadastrar a música: ") + str(e), "error")
            return redirect(url_for('routes.add_music'))
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    # Se a requisição for GET, apenas exibe o formulário
    return render_template('add_music.html')

# A rota de edição permanece como estava (se necessário)
@bp.route('/musics/edit/<int:id>', methods=['GET'])
def edit_music(id):
    # (Seu código de edição existente aqui... lembre-se de proteger a rota)
    pass