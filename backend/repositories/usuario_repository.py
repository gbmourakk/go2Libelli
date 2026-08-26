from sqlalchemy import text
from extensions import db
from repositories._util import normalizar_linha

class UsuarioRepository:
    @staticmethod
    def buscar_por_email(email):
        if db.session.get_bind().dialect.name == "mysql":
            resultado = db.session.execute(text("CALL sp_buscar_usuario_por_email(:p_email)"), {"p_email": email})
            linha = resultado.mappings().first(); resultado.close()
            if linha:
                dados = normalizar_linha(linha)
                from models.usuario import Usuario
                return Usuario.buscar_por_id(dados["id"])
        from models.usuario import Usuario
        return Usuario.buscar_por_email(email)

    @staticmethod
    def listar_com_disciplinas_count(usuario_id=None):
        if db.session.get_bind().dialect.name == "mysql":
            resultado = db.session.execute(text("CALL sp_listar_usuarios_com_disciplinas_count(:p_usuario_id)"), {"p_usuario_id": usuario_id})
            linhas = resultado.mappings().all(); resultado.close()
            return [normalizar_linha(l) for l in linhas]
        from models.usuario import Usuario
        query = Usuario.query
        if usuario_id is not None: query = query.filter(Usuario.id == usuario_id)
        return [{**u.to_dict(), "disciplinas_count": len(u.disciplinas)} for u in query.all()]
