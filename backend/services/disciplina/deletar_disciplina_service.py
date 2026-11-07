from models.disciplina import Disciplina

class DeletarDisciplinaService:
    def execute(self, disciplina_id):
        disciplina = Disciplina.buscar_por_id(disciplina_id)
        if not disciplina: return False
        disciplina.deletar()
        return True
