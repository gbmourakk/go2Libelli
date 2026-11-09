from services.conversa.buscar_conversa_service import BuscarConversaService


class ExcluirConversaService:
    def execute(self, usuario_id, conversa_id):
        conversa = BuscarConversaService().execute(usuario_id, conversa_id)
        if not conversa:
            return False
        conversa.deletar()
        return True
