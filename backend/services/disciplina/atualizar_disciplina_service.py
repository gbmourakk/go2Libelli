from models.disciplina import Disciplina

class AtualizarDisciplinaService:
    def execute(self, disciplina_id, dados):
        disciplina = Disciplina.buscar_por_id(disciplina_id)
        return disciplina.atualizar(nome=dados.get("nome"), descricao=dados.get("descricao")) if disciplina else None
