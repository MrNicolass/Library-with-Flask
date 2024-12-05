from flask import Blueprint

# Blueprint para as rotas
bp = Blueprint('routes', __name__)

# Importar rotas de outros arquivos
from .users import *
from .index import *
from .oAuth import *
from .musics import *