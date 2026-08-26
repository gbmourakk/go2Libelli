from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import db
from routes import register_routes



def _atualizar_schema_sqlite():
    """Mantém bancos SQLite antigos compatíveis com as Models atuais.

    O projeto foi refatorado para separar o texto gerado do relacionamento
    com Conteudo. Bancos criados antes dessa alteração podem não possuir as
    colunas de texto de Resumo e Quiz. SQLite não altera tabelas existentes
    com db.create_all(), então fazemos apenas essas alterações incrementais.
    """
    from sqlalchemy import inspect, text

    if db.session.get_bind().dialect.name != "sqlite":
        return

    inspector = inspect(db.engine)
    alteracoes = {
        "resumos": {"conteudo": "TEXT"},
        "quizzes": {"conteudo": "TEXT"},
    }

    for tabela, colunas in alteracoes.items():
        existentes = {coluna["name"] for coluna in inspector.get_columns(tabela)}
        for nome, tipo in colunas.items():
            if nome not in existentes:
                db.session.execute(text(f'ALTER TABLE {tabela} ADD COLUMN {nome} {tipo}'))

    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    register_routes(app)

    with app.app_context():
        import models  # noqa: F401
        db.create_all()
        _atualizar_schema_sqlite()

    @app.get("/api/health")
    def health():
        return {"status": "ok", "projeto": "LIBELLI"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
