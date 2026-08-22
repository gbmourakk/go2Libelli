from models.comentario import Comentario

class ListarComentariosService:
    def execute(self, disciplina_id=None):
        return Comentario.listar_por_disciplina(disciplina_id) if disciplina_id else Comentario.listar_todos()
