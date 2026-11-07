from models.conteudo import Conteudo
from models.quiz import Quiz
from services.motor_ia.motor_ia_service import MotorIAService

class GerarQuizService:
    def execute(self, conteudo_id, titulo=None):
        conteudo = Conteudo.buscar_por_id(conteudo_id)
        if not conteudo: raise ValueError("Conteúdo não encontrado.")
        texto = MotorIAService().execute("atividades", conteudo.conteudo or conteudo.titulo)
        return Quiz(titulo=titulo or f"Quiz de {conteudo.titulo or 'conteúdo'}", conteudo=texto, perguntas=texto,
                    disciplina_id=conteudo.disciplina_id, conteudo_id=conteudo.id).salvar()
