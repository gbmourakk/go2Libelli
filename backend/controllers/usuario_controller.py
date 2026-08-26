from flask import Blueprint, jsonify, request

from services.usuario.autenticar_usuario_service import AutenticarUsuarioService
from services.usuario.atualizar_usuario_service import AtualizarUsuarioService
from services.usuario.buscar_usuario_service import BuscarUsuarioService
from services.usuario.criar_usuario_service import CriarUsuarioService
from services.usuario.deletar_usuario_service import DeletarUsuarioService
from services.usuario.listar_usuarios_com_disciplinas_service import ListarUsuariosComDisciplinasService
from services.usuario.listar_usuarios_service import ListarUsuariosService


class UsuarioController:
    blueprint = Blueprint("usuario_controller", __name__)

    @staticmethod
    def listar():
        usuarios = ListarUsuariosService().execute()
        return jsonify([usuario.to_dict() for usuario in usuarios])

    @staticmethod
    def buscar(usuario_id):
        usuario = BuscarUsuarioService().execute(usuario_id)
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado."}), 404
        return jsonify(usuario.to_dict())

    @staticmethod
    def criar():
        try:
            usuario = CriarUsuarioService().execute(request.get_json() or {})
            return jsonify(usuario.to_dict()), 201
        except (ValueError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def atualizar(usuario_id):
        try:
            usuario = AtualizarUsuarioService().execute(
                usuario_id, request.get_json() or {}
            )
            if not usuario:
                return jsonify({"erro": "Usuário não encontrado."}), 404
            return jsonify(usuario.to_dict())
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def deletar(usuario_id):
        if not DeletarUsuarioService().execute(usuario_id):
            return jsonify({"erro": "Usuário não encontrado."}), 404
        return "", 204

    @staticmethod
    def login():
        dados = request.get_json() or {}
        if not dados.get("email") or not dados.get("senha"):
            return jsonify({"erro": "email e senha são obrigatórios."}), 400

        usuario = AutenticarUsuarioService().execute(
            dados["email"], dados["senha"]
        )
        if not usuario:
            return jsonify({"erro": "E-mail ou senha inválidos."}), 401
        return jsonify(usuario.to_dict())

    @staticmethod
    def listar_com_disciplinas():
        dados = ListarUsuariosComDisciplinasService().execute(
            request.args.get("usuario_id", type=int)
        )
        return jsonify(dados)


UsuarioController.blueprint.add_url_rule("/", view_func=UsuarioController.listar, methods=["GET"])
UsuarioController.blueprint.add_url_rule("/", view_func=UsuarioController.criar, methods=["POST"])
UsuarioController.blueprint.add_url_rule("/<int:usuario_id>", view_func=UsuarioController.buscar, methods=["GET"])
UsuarioController.blueprint.add_url_rule("/<int:usuario_id>", view_func=UsuarioController.atualizar, methods=["PUT"])
UsuarioController.blueprint.add_url_rule("/<int:usuario_id>", view_func=UsuarioController.deletar, methods=["DELETE"])
UsuarioController.blueprint.add_url_rule("/login", view_func=UsuarioController.login, methods=["POST"])
UsuarioController.blueprint.add_url_rule("/com-contagem", view_func=UsuarioController.listar_com_disciplinas, methods=["GET"])
