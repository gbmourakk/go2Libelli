from werkzeug.security import generate_password_hash
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository


class CriarUsuarioService:
    def execute(self, dados):
        if not dados.get("nome") or not dados.get("email") or not dados.get("senha"):
            raise ValueError("nome, email e senha são obrigatórios.")
        if UsuarioRepository.buscar_por_email(dados["email"]):
            raise ValueError("Já existe um usuário com este e-mail.")
        usuario = Usuario(nome=dados["nome"], email=dados["email"], senha_hash=generate_password_hash(dados["senha"]))
        return usuario.salvar()
