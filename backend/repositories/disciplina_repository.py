                                                

                                                                         
                                                       
   

from sqlalchemy import text

from extensions import db
from models.disciplina import Disciplina
from repositories._util import normalizar_linha


class DisciplinaRepository:
    @staticmethod
    def listar_por_usuario(usuario_id):
                                                                         
        if db.session.get_bind().dialect.name == "mysql":
            resultado = db.session.execute(
                text("CALL sp_listar_disciplinas_por_usuario(:p_usuario_id)"),
                {"p_usuario_id": usuario_id},
            )
            linhas = resultado.mappings().all()
            resultado.close()
            return [normalizar_linha(linha) for linha in linhas]

        ids = db.session.execute(
            text("SELECT id FROM disciplinas WHERE usuario_id = :usuario_id ORDER BY id"),
            {"usuario_id": usuario_id},
        ).scalars().all()
        return [Disciplina.buscar_por_id(identificador) for identificador in ids]

    @staticmethod
    def listar_com_contagem(usuario_id=None):
                                                                                
        if db.session.get_bind().dialect.name == "mysql":
            resultado = db.session.execute(
                text("CALL sp_listar_disciplinas_com_materiais_count(:p_usuario_id)"),
                {"p_usuario_id": usuario_id},
            )
            linhas = resultado.mappings().all()
            resultado.close()
            return [normalizar_linha(linha) for linha in linhas]

        linhas = db.session.execute(
            text("""
                SELECT d.id,
                    (SELECT COUNT(*) FROM conteudos c WHERE c.disciplina_id = d.id) +
                    (SELECT COUNT(*) FROM comentarios c WHERE c.disciplina_id = d.id) +
                    (SELECT COUNT(*) FROM quizzes q WHERE q.disciplina_id = d.id) +
                    (SELECT COUNT(*) FROM resumos r WHERE r.disciplina_id = d.id) +
                    (SELECT COUNT(*) FROM revisoes v WHERE v.disciplina_id = d.id)
                    AS materiais_count
                FROM disciplinas d
                WHERE (:usuario_id IS NULL OR d.usuario_id = :usuario_id)
                ORDER BY d.id
            """),
            {"usuario_id": usuario_id},
        ).mappings().all()

        return [
            {**Disciplina.buscar_por_id(linha["id"]).to_dict(),
             "materiais_count": linha["materiais_count"]}
            for linha in linhas
        ]
