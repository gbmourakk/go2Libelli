from models.conteudo import Conteudo

class AtualizarConteudoService:
    def execute(self, item_id, dados):
        item = Conteudo.buscar_por_id(item_id)
        if not item: return None
        permitidos = Conteudo.permitidos()
        return item.atualizar(**{k: v for k, v in dados.items() if k in permitidos})
