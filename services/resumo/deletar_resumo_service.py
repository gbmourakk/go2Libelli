from models.resumo import Resumo

class DeletarResumoService:
    def execute(self, item_id):
        item = Resumo.buscar_por_id(item_id)
        if not item: return False
        item.deletar()
        return True
