from models.resumo import Resumo

class AtualizarResumoService:
    def execute(self, item_id, dados):
        item = Resumo.buscar_por_id(item_id)
        if not item: return None
        permitidos = Resumo.permitidos()
        return item.atualizar(**{k: v for k, v in dados.items() if k in permitidos})
