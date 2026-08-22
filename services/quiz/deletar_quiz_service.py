from models.quiz import Quiz

class DeletarQuizService:
    def execute(self, item_id):
        item = Quiz.buscar_por_id(item_id)
        if not item: return False
        item.deletar()
        return True
