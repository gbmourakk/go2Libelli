from sqlalchemy import text
from extensions import db
from repositories._util import normalizar_linha

class DisciplinaRepository:
    @staticmethod
    def listar_por_usuario(usuario_id):
        if db.session.get_bind().dialect.name == "mysql":
            resultado = db.session.execute(text("CALL sp_listar_disciplinas_por_usuario(:p_usuario_id)"), {"p_usuario_id": usuario_id})
            linhas = resultado.mappings().all(); resultado.close()
            return [normalizar_linha(l) for l in linhas]
        from models.disciplina import Disciplina
        return Disciplina.listar_por_usuario(usuario_id)

    @staticmethod
    def listar_com_contagem(usuario_id=None):
        if db.session.get_bind().dialect.name == "mysql":
            resultado = db.session.execute(text("CALL sp_listar_disciplinas_com_materiais_count(:p_usuario_id)"), {"p_usuario_id": usuario_id})
            linhas = resultado.mappings().all(); resultado.close()
            return [normalizar_linha(l) for l in linhas]
        from models.disciplina import Disciplina
        query = Disciplina.query
        if usuario_id is not None: query = query.filter(Disciplina.usuario_id == usuario_id)
        return [{**d.to_dict(), "materiais_count": len(d.conteudos)+len(d.comentarios)+len(d.quizzes)+len(d.resumos)+len(d.revisoes)} for d in query.all()]
