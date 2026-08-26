from models.comentario import Comentario

class AtualizarComentarioService:
    def execute(self, item_id, dados):
        item = Comentario.buscar_por_id(item_id)
        if not item: return None
        permitidos = Comentario.permitidos()
        return item.atualizar(**{k: v for k, v in dados.items() if k in permitidos})
