from models.disciplina import Disciplina
from models.plano_estudo import PlanoEstudo
from services.motor_ia.motor_ia_service import MotorIAService


class GerarPlanoEstudoService:
    DIFICULDADES = {"iniciante", "intermediario", "avancado"}

    def execute(self, usuario_id, dados):
        if not isinstance(dados, dict):
            raise ValueError("Envie os dados do plano em JSON.")

        try:
            disciplina_id = int(dados.get("disciplina_id"))
        except (ValueError, TypeError):
            raise ValueError("Selecione uma disciplina válida.") from None

        disciplina = Disciplina.buscar_por_id(disciplina_id)
        if not disciplina or disciplina.usuario_id != usuario_id:
            raise ValueError("Disciplina não encontrada para este usuário.")

        tema = dados.get("tema")
        if not isinstance(tema, str) or not (3 <= len(tema.strip()) <= 200):
            raise ValueError("Informe um assunto de 3 a 200 caracteres.")
        tema = tema.strip()

        def ler_inteiro(valor):
            # Não aceita decimais (2.5), booleanos nem texto arbitrário.
            if isinstance(valor, bool) or not str(valor).strip().isdigit():
                raise ValueError("Dias e minutos devem ser números inteiros.")
            return int(valor)

        dias = ler_inteiro(dados.get("dias"))
        minutos_por_dia = ler_inteiro(dados.get("minutos_por_dia"))

        if not 1 <= dias <= 30:
            raise ValueError("O prazo deve ser de 1 a 30 dias.")
        if not 15 <= minutos_por_dia <= 480:
            raise ValueError("O tempo diário deve ser de 15 a 480 minutos.")

        dificuldade = dados.get("dificuldade", "iniciante")
        if not isinstance(dificuldade, str) or dificuldade not in self.DIFICULDADES:
            raise ValueError("Dificuldade inválida.")

        instrucoes = (
            f"Disciplina: {disciplina.nome}\n"
            f"Assunto: {tema}\n"
            f"Prazo: {dias} dia(s)\n"
            f"Tempo disponível por dia: {minutos_por_dia} minutos\n"
            f"Nível de conhecimento: {dificuldade}\n"
            "Crie uma sequência de atividades que respeite rigorosamente esses limites."
        )
        cronograma = MotorIAService().execute("plano", instrucoes)

        # Só persiste depois que a IA devolve uma resposta bem-sucedida.
        return PlanoEstudo(
            titulo=f"Plano: {tema}"[:150],
            tema=tema,
            dias=dias,
            minutos_por_dia=minutos_por_dia,
            dificuldade=dificuldade,
            cronograma=cronograma,
            disciplina_id=disciplina.id,
        ).salvar()
