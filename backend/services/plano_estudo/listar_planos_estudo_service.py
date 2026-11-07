from models.plano_estudo import PlanoEstudo


class ListarPlanosEstudoService:
    def execute(self, usuario_id):
        return PlanoEstudo.listar_por_usuario(usuario_id)
