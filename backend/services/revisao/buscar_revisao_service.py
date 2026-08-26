from models.revisao import Revisao

class BuscarRevisaoService:
    def execute(self, item_id):
        return Revisao.buscar_por_id(item_id)
