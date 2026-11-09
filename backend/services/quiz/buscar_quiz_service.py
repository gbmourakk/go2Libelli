from models.quiz import Quiz

class BuscarQuizService:
    def execute(self, item_id):
        return Quiz.buscar_por_id(item_id)
