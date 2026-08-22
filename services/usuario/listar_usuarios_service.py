from models.usuario import Usuario

class ListarUsuariosService:
    def execute(self):
        return Usuario.listar_todos()
