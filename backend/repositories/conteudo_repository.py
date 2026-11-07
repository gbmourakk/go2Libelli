"""Consultas específicas da entidade Conteudo.

Não representa um novo Model. Recupera apenas Conteudos das disciplinas
pertencentes a um usuário; o Service combina com os demais materiais.
"""

from sqlalchemy import text

from extensions import db
from models.conteudo import Conteudo


class ConteudoRepository:
    @staticmethod
    def listar_para_busca(usuario_id, disciplina_id=None):
        """SELECT com JOIN e parâmetros; retorna Models Conteudo para o Service.

        O filtro de texto é aplicado pelo BuscarEstudosService, junto aos
        demais tipos, preservando a comparação de texto usada antes.
        """
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
