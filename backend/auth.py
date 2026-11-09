
from flask import g, jsonify, request, session

from models.usuario import Usuario
from models.disciplina import Disciplina
from models.conteudo import Conteudo
from models.comentario import Comentario
from models.resumo import Resumo
from models.quiz import Quiz
from models.revisao import Revisao
from models.plano_estudo import PlanoEstudo

                                                 
MODELOS = {
    "disciplinas": Disciplina,
    "conteudos": Conteudo,
    "comentarios": Comentario,
    "resumos": Resumo,
    "quizzes": Quiz,
    "revisoes": Revisao,
    "planos": PlanoEstudo,
}


def erro(mensagem, codigo):
    return jsonify({"erro": mensagem}), codigo


def pertence_ao_usuario(registro, usuario_id):
                                                                                      
    if not registro:
        return False
    if isinstance(registro, Disciplina):
        return registro.usuario_id == usuario_id
    return bool(registro.disciplina and registro.disciplina.usuario_id == usuario_id)


def verificar_referencia(modelo, identificador, usuario_id):
                                                                                  
    try:
        registro = modelo.buscar_por_id(int(identificador))
    except (TypeError, ValueError):
        return erro("Identificador inválido.", 400)
    if not registro:
        return erro("Registro relacionado não encontrado.", 404)
    if not pertence_ao_usuario(registro, usuario_id):
        return erro("Este material não pertence à sua conta.", 403)
    return None


def verificar_acesso():
                                                             
    if not request.path.startswith("/api/") or request.method == "OPTIONS":
        return None

    partes = request.path[len("/api/"):].strip("/").split("/")
    recurso = partes[0]

                                                                           
    if recurso == "health":
        return None
    if recurso == "usuarios" and request.method == "POST" and (
        len(partes) == 1 or partes[1] == "login"
    ):
        return None

    usuario_id = session.get("usuario_id")
    usuario = Usuario.buscar_por_id(usuario_id) if isinstance(usuario_id, int) else None
    if not usuario:
        session.clear()
        return erro("Faça login para continuar.", 401)
    g.usuario = usuario

                                                                         
                                                                         
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        if request.headers.get("X-Libelli-Request") != "1":
            return erro("Requisição não autorizada.", 403)

                                                                          
    if recurso == "usuarios":
        if len(partes) > 1 and partes[1] in {"me", "logout"}:
            return None
        if len(partes) > 1 and partes[1].isdigit() and int(partes[1]) == usuario.id:
            return None
        return erro("Você só pode acessar sua própria conta.", 403)

    if recurso not in MODELOS:
        return None                                          

                                                                   
                                                                    
    parametros = request.args if request.method == "GET" else (request.get_json(silent=True) or {})
    if not hasattr(parametros, "get"):
        return erro("Dados inválidos.", 400)

    filtro_usuario = parametros.get("usuario_id")
    if filtro_usuario is not None and str(filtro_usuario) != str(usuario.id):
        return erro("Você não pode acessar dados de outra conta.", 403)

                                                                                   
    if request.method == "GET" and len(partes) == 1:
        if recurso in {"disciplinas", "planos"} and filtro_usuario is None:
            return erro("usuario_id é obrigatório.", 400)
        if recurso not in {"disciplinas", "planos"} and not parametros.get("disciplina_id"):
            return erro("disciplina_id é obrigatório.", 400)
    if recurso == "disciplinas" and len(partes) > 1 and partes[1] == "com-contagem":
        if filtro_usuario is None:
            return erro("usuario_id é obrigatório.", 400)

                                                              
    if len(partes) > 1 and partes[1].isdigit():
        registro = MODELOS[recurso].buscar_por_id(int(partes[1]))
        if not registro:
            return erro("Registro não encontrado.", 404)
        if not pertence_ao_usuario(registro, usuario.id):
            return erro("Este material não pertence à sua conta.", 403)

                                                                   
    for campo, modelo in (("disciplina_id", Disciplina), ("conteudo_id", Conteudo)):
        identificador = parametros.get(campo)
        if identificador is not None and identificador != "":
            falha = verificar_referencia(modelo, identificador, usuario.id)
            if falha:
                return falha

                                                                    
                                                                
    return None
