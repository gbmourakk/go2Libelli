from models.conteudo import Conteudo
from models.resumo import Resumo
from services.motor_ia.motor_ia_service import MotorIAService

class GerarResumoService:
    def execute(self, conteudo_id, titulo=None):
        conteudo = Conteudo.buscar_por_id(conteudo_id)
        if not conteudo: raise ValueError("Conteúdo não encontrado.")
        texto = MotorIAService().execute("resumo", conteudo.conteudo or conteudo.titulo)
        return Resumo(titulo=titulo or f"Resumo de {conteudo.titulo or 'conteúdo'}", conteudo=texto,
                       gerado_por_ia=True, disciplina_id=conteudo.disciplina_id, conteudo_id=conteudo.id).salvar()
