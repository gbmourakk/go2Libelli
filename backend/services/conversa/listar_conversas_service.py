from models.conversa import Conversa


class ListarConversasService:
    def execute(self, usuario_id):
        return Conversa.listar_por_usuario(usuario_id)
