from services.plano_estudo.buscar_plano_estudo_service import BuscarPlanoEstudoService


class DeletarPlanoEstudoService:
    def execute(self, usuario_id, plano_id):
        plano = BuscarPlanoEstudoService().execute(usuario_id, plano_id)
        if not plano:
            return False
        plano.deletar()
        return True
