from models.conversa import Conversa


class BuscarConversaService:
    def execute(self, usuario_id, conversa_id):
        return Conversa.buscar_do_usuario(conversa_id, usuario_id)
