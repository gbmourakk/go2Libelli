from models.disciplina import Disciplina

class ListarDisciplinasService:
    def execute(self, usuario_id=None):
        return Disciplina.listar_por_usuario(usuario_id) if usuario_id else Disciplina.listar_todos()
