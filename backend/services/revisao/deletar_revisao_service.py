from models.revisao import Revisao

class DeletarRevisaoService:
    def execute(self, item_id):
        item = Revisao.buscar_por_id(item_id)
        if not item: return False
        item.deletar()
        return True
