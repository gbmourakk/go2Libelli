from sqlalchemy import text
from extensions import db
from repositories._util import normalizar_linha

class EstudoRepository:
    """Consulta complexa que cruza as Models de estudo. Não representa uma Model."""
    @staticmethod
    def buscar(usuario_id, termo=None, disciplina_id=None, tipo=None, ordenar_por="criado_em", direcao="DESC"):
        if usuario_id is None:
            raise ValueError("usuario_id é obrigatório para a busca.")
        ordenar_por = (ordenar_por or "criado_em").lower()
        if ordenar_por not in {"criado_em", "titulo", "tipo", "disciplina"}:
            raise ValueError("ordenar_por inválido.")
        direcao = (direcao or "DESC").upper()
        if direcao not in {"ASC", "DESC"}:
            raise ValueError("direcao inválida. Use ASC ou DESC.")
        if db.session.get_bind().dialect.name == "mysql":
            resultado = db.session.execute(text("CALL sp_buscar_estudos(:p_usuario_id, :p_termo, :p_disciplina_id, :p_tipo, :p_ordenar_por, :p_direcao)"), {"p_usuario_id":usuario_id,"p_termo":termo,"p_disciplina_id":disciplina_id,"p_tipo":tipo,"p_ordenar_por":ordenar_por,"p_direcao":direcao})
            linhas=resultado.mappings().all(); resultado.close()
            return [normalizar_linha(l) for l in linhas]
        # SQLite fallback: combine the independent Models, preserving the old /anotacoes/buscar behavior.
        from models.disciplina import Disciplina
        from models.conteudo import Conteudo
        from models.comentario import Comentario
        from models.quiz import Quiz
        from models.resumo import Resumo
        from models.revisao import Revisao
        disciplinas = {d.id:d.nome for d in Disciplina.query.filter_by(usuario_id=usuario_id).all()}
        itens=[]
        for model in (Conteudo, Comentario, Quiz, Resumo, Revisao):
            for item in model.query.filter(model.disciplina_id.in_(list(disciplinas) or [-1])).all():
                d=item.to_dict(); d["disciplina_nome"]=disciplinas.get(item.disciplina_id)
                if termo and termo.lower() not in f"{d.get('titulo') or ''} {d.get('conteudo') or ''}".lower(): continue
                if disciplina_id is not None and item.disciplina_id != disciplina_id: continue
                if tipo and d.get("tipo") != tipo: continue
                itens.append(d)
        key = "disciplina_nome" if ordenar_por == "disciplina" else ordenar_por
        itens.sort(key=lambda x: (x.get(key) or ""), reverse=direcao == "DESC")
        return itens
