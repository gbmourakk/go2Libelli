from models.disciplina import Disciplina

class CriarDisciplinaService:
    def execute(self, dados):
        if not dados.get("nome") or not dados.get("usuario_id"):
            raise ValueError("nome e usuario_id são obrigatórios.")
        return Disciplina(nome=dados["nome"], descricao=dados.get("descricao"), usuario_id=dados["usuario_id"]).salvar()
