from models.resumo import Resumo

class ListarResumosService:
    def execute(self, disciplina_id=None):
        return Resumo.listar_por_disciplina(disciplina_id) if disciplina_id else Resumo.listar_todos()
