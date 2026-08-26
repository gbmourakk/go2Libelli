from repositories.estudo_repository import EstudoRepository


class BuscarEstudosService:
    def execute(
        self,
        usuario_id,
        termo=None,
        disciplina_id=None,
        tipo=None,
        ordenar_por="criado_em",
        direcao="desc",
    ):
        return EstudoRepository.buscar(
            usuario_id=usuario_id,
            termo=termo,
            disciplina_id=disciplina_id,
            tipo=tipo,
            ordenar_por=ordenar_por,
            direcao=direcao,
        )
