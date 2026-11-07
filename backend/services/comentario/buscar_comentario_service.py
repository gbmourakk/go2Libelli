from models.comentario import Comentario

class BuscarComentarioService:
    def execute(self, item_id):
        return Comentario.buscar_por_id(item_id)
