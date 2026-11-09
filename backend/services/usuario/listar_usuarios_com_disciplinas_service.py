from repositories.usuario_repository import UsuarioRepository

class ListarUsuariosComDisciplinasService:
    def execute(self, usuario_id=None):
        return UsuarioRepository.listar_com_disciplinas_count(usuario_id)
