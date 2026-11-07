from models.conteudo import Conteudo

class BuscarConteudoService:
    def execute(self, item_id):
        return Conteudo.buscar_por_id(item_id)
