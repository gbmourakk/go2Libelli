from repositories.disciplina_repository import DisciplinaRepository


class ListarDisciplinasComContagemService:
    def execute(self, usuario_id=None):
        return DisciplinaRepository.listar_com_contagem(usuario_id)
