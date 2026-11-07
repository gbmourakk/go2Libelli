from models.comentario import Comentario

class DeletarComentarioService:
    def execute(self, item_id):
        item = Comentario.buscar_por_id(item_id)
        if not item: return False
        item.deletar()
        return True
