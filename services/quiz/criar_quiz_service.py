from models.quiz import Quiz


class CriarQuizService:
    def execute(self, dados):
        if not dados.get("disciplina_id"):
            raise ValueError("disciplina_id é obrigatório.")

        quiz = Quiz(
            titulo=dados.get("titulo"),
            conteudo=dados.get("conteudo"),
            perguntas=dados.get("perguntas"),
            disciplina_id=dados["disciplina_id"],
            conteudo_id=dados.get("conteudo_id", dados.get("pai_id")),
        )
        return quiz.salvar()
