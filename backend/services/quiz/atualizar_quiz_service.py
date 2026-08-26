from models.quiz import Quiz

class AtualizarQuizService:
    def execute(self, item_id, dados):
        item = Quiz.buscar_por_id(item_id)
        if not item: return None
        permitidos = Quiz.permitidos()
        return item.atualizar(**{k: v for k, v in dados.items() if k in permitidos})
