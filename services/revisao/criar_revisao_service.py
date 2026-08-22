from models.revisao import Revisao


class CriarRevisaoService:
    def execute(self, dados):
        if not dados.get("disciplina_id"):
            raise ValueError("disciplina_id é obrigatório.")

        revisao = Revisao(
            titulo=dados.get("titulo"),
            conteudo=dados.get("conteudo"),
            data_revisao=dados.get("data_revisao"),
            status=dados.get("status", "pendente"),
            disciplina_id=dados["disciplina_id"],
            conteudo_id=dados.get("conteudo_id", dados.get("pai_id")),
        )
        return revisao.salvar()
