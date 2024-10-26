from flask import Flask
from database.dbFunctions import init_app, init_db
from routes import bp as routes_bp
from routes.oAuth import blueprint as google_blueprint
from routes.oAuth import github_blueprint

app = Flask(__name__, template_folder= "pages")
app.config["SECRET_KEY"] = "random string"

# Inicializar o banco de dados
init_app(app)

app.register_blueprint(google_blueprint, url_prefix="/loginOAuthGoogle")
app.register_blueprint(github_blueprint, url_prefix="/loginOAuthGithub")

# Registrar o Blueprint das rotas
app.register_blueprint(routes_bp)

@app.route('/initdb')
def initialize_db():
    init_db()
    return "<a href='/'>Banco de dados inicializado!</a>"

#Starts server in debug mode
if __name__ == '__main__':
    app.run(debug=True, port=5000) 