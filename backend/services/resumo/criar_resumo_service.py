from models.resumo import Resumo


class CriarResumoService:
    def execute(self, dados):
        if not dados.get("disciplina_id"):
            raise ValueError("disciplina_id é obrigatório.")

        resumo = Resumo(
            titulo=dados.get("titulo"),
            conteudo=dados.get("conteudo"),
            gerado_por_ia=dados.get("gerado_por_ia", False),
            disciplina_id=dados["disciplina_id"],
            conteudo_id=dados.get("conteudo_id", dados.get("pai_id")),
        )
        return resumo.salvar()
