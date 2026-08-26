from models.revisao import Revisao

class AtualizarRevisaoService:
    def execute(self, item_id, dados):
        item = Revisao.buscar_por_id(item_id)
        if not item: return None
        permitidos = Revisao.permitidos()
        return item.atualizar(**{k: v for k, v in dados.items() if k in permitidos})
