import os
from flask import Flask
from flask_cors import CORS
from extensions import db
import models
from models.usuario import Usuario
from models.disciplina import Disciplina
from models.conteudo import Conteudo
from models.resumo import Resumo
from services.usuario.criar_usuario_service import CriarUsuarioService
from services.disciplina.criar_disciplina_service import CriarDisciplinaService
from services.conteudo.criar_conteudo_service import CriarConteudoService
from services.resumo.gerar_resumo_service import GerarResumoService

DB_FILE="quick_test.db"
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=f"sqlite:///{DB_FILE}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
CORS(app); db.init_app(app)

with app.app_context():
    db.drop_all(); db.create_all()
    usuario=CriarUsuarioService().execute({"nome":"Ana","email":"ana@teste.com","senha":"123456"})
    disciplina=CriarDisciplinaService().execute({"nome":"Banco de Dados II","descricao":"Normalização e SQL","usuario_id":usuario.id})
    conteudo=CriarConteudoService().execute({"tipo":"conteudo","titulo":"Aula 1 - Normalização","conteudo":"1FN, 2FN, 3FN...","disciplina_id":disciplina.id})
    resumo=GerarResumoService().execute(conteudo.id)
    print(usuario.to_dict()); print(disciplina.to_dict()); print(conteudo.to_dict()); print(resumo.to_dict())
    print("Tudo certo! ")
    db.session.remove()
if os.path.exists(DB_FILE): os.remove(DB_FILE)
