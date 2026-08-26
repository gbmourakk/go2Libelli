from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from werkzeug.security import generate_password_hash

class AtualizarUsuarioService:
    def execute(self, usuario_id, dados):
        usuario = Usuario.buscar_por_id(usuario_id)
        if not usuario:
            return None
        email = dados.get("email")
        if email and email != usuario.email and UsuarioRepository.buscar_por_email(email):
            raise ValueError("Já existe outro usuário com este e-mail.")
        senha_hash = generate_password_hash(dados["senha"]) if dados.get("senha") else None
        return usuario.atualizar(nome=dados.get("nome"), email=email, senha_hash=senha_hash)
