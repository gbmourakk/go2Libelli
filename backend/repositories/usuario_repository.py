"""Consultas específicas da entidade Usuario.

CRUD simples continua no Model Usuario. As consultas SQL usam parâmetros,
sem concatenar valores recebidos do usuário na instrução.
"""

from sqlalchemy import text

from extensions import db
from models.usuario import Usuario
from repositories._util import normalizar_linha


class UsuarioRepository:
    @staticmethod
    def buscar_por_email(email):
        """Retorna Usuario (Model), ou None; usado no cadastro e no login."""
        if db.session.get_bind().dialect.name == "mysql":
            resultado = db.session.execute(
                text("CALL sp_buscar_usuario_por_email(:p_email)"),
                {"p_email": email},
            )
            linha = resultado.mappings().first()
            resultado.close()
            usuario_id = linha["id"] if linha else None
        else:
            # SQL explícito no SQLite: não expõe senha_hash na resposta da API.
            usuario_id = db.session.execute(
                text("SELECT id FROM usuarios WHERE email = :email LIMIT 1"),
                {"email": email},
            ).scalar()
        return Usuario.buscar_por_id(usuario_id) if usuario_id is not None else None

    @staticmethod
    def listar_com_disciplinas_count(usuario_id=None):
        """Conta disciplinas por usuário sem carregar todas as relações no Python."""
        if db.session.get_bind().dialect.name == "mysql":
            resultado = db.session.execute(
                text("CALL sp_listar_usuarios_com_disciplinas_count(:p_usuario_id)"),
                {"p_usuario_id": usuario_id},
            )
            linhas = resultado.mappings().all()
            resultado.close()
            return [normalizar_linha(linha) for linha in linhas]

        linhas = db.session.execute(
            text("""
                SELECT u.id, COUNT(d.id) AS disciplinas_count
                FROM usuarios AS u
                LEFT JOIN disciplinas AS d ON d.usuario_id = u.id
                WHERE (:usuario_id IS NULL OR u.id = :usuario_id)
                GROUP BY u.id
                ORDER BY u.id
            """),
            {"usuario_id": usuario_id},
        ).mappings().all()

        return [
            {**Usuario.buscar_por_id(linha["id"]).to_dict(),
             "disciplinas_count": linha["disciplinas_count"]}
            for linha in linhas
        ]
