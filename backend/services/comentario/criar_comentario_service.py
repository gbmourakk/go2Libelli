from models.comentario import Comentario


class CriarComentarioService:
    def execute(self, dados):
        if not dados.get("disciplina_id"):
            raise ValueError("disciplina_id é obrigatório.")

        comentario = Comentario(
            titulo=dados.get("titulo"),
            texto=dados.get("texto", dados.get("conteudo")),
            disciplina_id=dados["disciplina_id"],
            conteudo_id=dados.get("conteudo_id", dados.get("pai_id")),
        )
        return comentario.salvar()
