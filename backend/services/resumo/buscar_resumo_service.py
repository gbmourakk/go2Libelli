from models.resumo import Resumo

class BuscarResumoService:
    def execute(self, item_id):
        return Resumo.buscar_por_id(item_id)
