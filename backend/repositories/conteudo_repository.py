                                              

                                                                       
                                                                     
   

from sqlalchemy import text

from extensions import db
from models.conteudo import Conteudo


class ConteudoRepository:
    @staticmethod
    def listar_para_busca(usuario_id, disciplina_id=None):
                                                                                

                                                                         
                                                                    
           
        ids = db.session.execute(
            text("""
                SELECT c.id
                FROM conteudos c
                INNER JOIN disciplinas d ON d.id = c.disciplina_id
                WHERE d.usuario_id = :usuario_id
                    AND (:disciplina_id IS NULL OR c.disciplina_id = :disciplina_id)
                ORDER BY c.id
            """),
            {"usuario_id": usuario_id, "disciplina_id": disciplina_id},
        ).scalars().all()
        return [Conteudo.buscar_por_id(identificador) for identificador in ids]
