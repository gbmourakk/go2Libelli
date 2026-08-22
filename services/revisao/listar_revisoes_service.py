from models.revisao import Revisao


class ListarRevisoesService:
    def execute(self, disciplina_id=None):
        return (
            Revisao.listar_por_disciplina(disciplina_id)
            if disciplina_id
            else Revisao.listar_todos()
        )