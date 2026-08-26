from models.conteudo import Conteudo
from models.revisao import Revisao

class GerarRevisaoService:
    def execute(self, conteudo_id, data_revisao):
        conteudo = Conteudo.buscar_por_id(conteudo_id)
        if not conteudo: raise ValueError("Conteúdo não encontrado.")
        return Revisao(titulo=f"Revisão de {conteudo.titulo or 'conteúdo'}", data_revisao=data_revisao,
                       status="pendente", disciplina_id=conteudo.disciplina_id, conteudo_id=conteudo.id).salvar()
