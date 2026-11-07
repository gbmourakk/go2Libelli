from models.quiz import Quiz


class ListarQuizzesService:
    def execute(self, disciplina_id=None):
        return Quiz.listar_por_disciplina(disciplina_id) if disciplina_id else Quiz.listar_todos()
