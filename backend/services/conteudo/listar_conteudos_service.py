from models.conteudo import Conteudo

class ListarConteudosService:
    def execute(self, disciplina_id=None):
        return Conteudo.listar_por_disciplina(disciplina_id) if disciplina_id else Conteudo.listar_todos()
