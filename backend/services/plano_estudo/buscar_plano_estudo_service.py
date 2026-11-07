from models.plano_estudo import PlanoEstudo


class BuscarPlanoEstudoService:
    def execute(self, usuario_id, plano_id):
        plano = PlanoEstudo.buscar_por_id(plano_id)
        if not plano or plano.disciplina.usuario_id != usuario_id:
            return None
        return plano
