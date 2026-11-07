from models.usuario import Usuario

class DeletarUsuarioService:
    def execute(self, usuario_id):
        usuario = Usuario.buscar_por_id(usuario_id)
        if not usuario:
            return False
        usuario.deletar()
        return True
