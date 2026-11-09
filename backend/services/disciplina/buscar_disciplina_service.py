from models.disciplina import Disciplina

class BuscarDisciplinaService:
    def execute(self, disciplina_id):
        return Disciplina.buscar_por_id(disciplina_id)
