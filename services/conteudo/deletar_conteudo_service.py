from models.conteudo import Conteudo

class DeletarConteudoService:
    def execute(self, item_id):
        item = Conteudo.buscar_por_id(item_id)
        if not item: return False
        item.deletar()
        return True
