from models.disciplina import Disciplina
from models.comentario import Comentario
from models.quiz import Quiz
from models.resumo import Resumo
from models.revisao import Revisao
from repositories.conteudo_repository import ConteudoRepository


class BuscarEstudosService:
    def execute(
        self,
        usuario_id,
        termo=None,
        disciplina_id=None,
        tipo=None,
        ordenar_por="criado_em",
        direcao="desc",
    ):
        if usuario_id is None:
            raise ValueError("usuario_id é obrigatório para a busca.")
        ordenar_por = (ordenar_por or "criado_em").lower()
        if ordenar_por not in {"criado_em", "titulo", "tipo", "disciplina"}:
            raise ValueError("ordenar_por inválido.")
        direcao = (direcao or "DESC").upper()
        if direcao not in {"ASC", "DESC"}:
            raise ValueError("direcao inválida. Use ASC ou DESC.")

                                                                  
        disciplinas = {
            disciplina.id: disciplina.nome
            for disciplina in Disciplina.query.filter_by(usuario_id=usuario_id).all()
        }
        ids = list(disciplinas)
        if disciplina_id is not None:
            if disciplina_id not in disciplinas:
                return []
            ids = [disciplina_id]
        if not ids:
            return []

        itens = []

        def acrescentar(registros):
            for registro in registros:
                dados = registro.to_dict()
                dados["disciplina_nome"] = disciplinas.get(registro.disciplina_id)
                if termo and termo.lower() not in (
                    f"{dados.get('titulo') or ''} {dados.get('conteudo') or ''}"
                ).lower():
                    continue
                if tipo and dados.get("tipo") != tipo:
                    continue
                itens.append(dados)

        if not tipo or tipo == "conteudo":
            acrescentar(ConteudoRepository.listar_para_busca(usuario_id, disciplina_id))

        for model, nome_tipo in (
            (Comentario, "comentario"),
            (Quiz, "quiz"),
            (Resumo, "resumo"),
            (Revisao, "revisao"),
        ):
            if not tipo or tipo == nome_tipo:
                acrescentar(model.query.filter(model.disciplina_id.in_(ids)).all())

        chave = "disciplina_nome" if ordenar_por == "disciplina" else ordenar_por
        itens.sort(key=lambda item: (item.get(chave) or ""), reverse=direcao == "DESC")
        return itens
