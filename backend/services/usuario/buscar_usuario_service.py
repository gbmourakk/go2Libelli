from models.usuario import Usuario

class BuscarUsuarioService:
    def execute(self, usuario_id):
        return Usuario.buscar_por_id(usuario_id)
