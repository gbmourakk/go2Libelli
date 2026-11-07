from werkzeug.security import check_password_hash
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository

class AutenticarUsuarioService:
    def execute(self, email, senha):
        usuario = UsuarioRepository.buscar_por_email(str(email).strip().lower())
        if not usuario or not check_password_hash(usuario.senha_hash, senha):
            return None
        return usuario
