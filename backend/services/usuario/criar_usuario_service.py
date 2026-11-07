from werkzeug.security import generate_password_hash
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository


class CriarUsuarioService:
    def execute(self, dados):
        nome = str(dados.get("nome") or "").strip()
        email = str(dados.get("email") or "").strip().lower()
        senha = dados.get("senha") or ""
        if len(nome) < 2 or len(nome) > 120:
            raise ValueError("Informe um nome entre 2 e 120 caracteres.")
        if len(email) > 150 or "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Informe um e-mail válido.")
        if not isinstance(senha, str) or len(senha) < 8:
            raise ValueError("A senha deve ter no mínimo 8 caracteres.")
        if UsuarioRepository.buscar_por_email(email):
            raise ValueError("Já existe um usuário com este e-mail.")
        usuario = Usuario(nome=nome, email=email, senha_hash=generate_password_hash(senha))
        return usuario.salvar()
