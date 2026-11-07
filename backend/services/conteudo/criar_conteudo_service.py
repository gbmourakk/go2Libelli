from models.conteudo import Conteudo


class CriarConteudoService:
    def execute(self, dados):
        if not dados.get("disciplina_id"):
            raise ValueError("disciplina_id é obrigatório.")

        conteudo = Conteudo(
            titulo=dados.get("titulo"),
            conteudo=dados.get("conteudo"),
            disciplina_id=dados["disciplina_id"],
        )
        return conteudo.salvar()
