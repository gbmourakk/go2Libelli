from flask import Blueprint, jsonify, request

from services.comentario.atualizar_comentario_service import AtualizarComentarioService
from services.comentario.buscar_comentario_service import BuscarComentarioService
from services.comentario.criar_comentario_service import CriarComentarioService
from services.comentario.deletar_comentario_service import DeletarComentarioService
from services.comentario.listar_comentarios_service import ListarComentariosService


class ComentarioController:
    blueprint = Blueprint("comentario_controller", __name__)

    @staticmethod
    def listar():
        comentarios = ListarComentariosService().execute(
            request.args.get("disciplina_id", type=int)
        )
        return jsonify([comentario.to_dict() for comentario in comentarios])

    @staticmethod
    def buscar(comentario_id):
        comentario = BuscarComentarioService().execute(comentario_id)
        if not comentario:
            return jsonify({"erro": "Comentário não encontrado."}), 404
        return jsonify(comentario.to_dict())

    @staticmethod
    def criar():
        try:
            comentario = CriarComentarioService().execute(request.get_json() or {})
            return jsonify(comentario.to_dict()), 201
        except (ValueError, KeyError) as erro:
            return jsonify({"erro": str(erro)}), 400

    @staticmethod
    def atualizar(comentario_id):
        comentario = AtualizarComentarioService().execute(
            comentario_id, request.get_json() or {}
        )
        if not comentario:
            return jsonify({"erro": "Comentário não encontrado."}), 404
        return jsonify(comentario.to_dict())

    @staticmethod
    def deletar(comentario_id):
        if not DeletarComentarioService().execute(comentario_id):
            return jsonify({"erro": "Comentário não encontrado."}), 404
        return "", 204


ComentarioController.blueprint.add_url_rule("/", view_func=ComentarioController.listar, methods=["GET"])
ComentarioController.blueprint.add_url_rule("/", view_func=ComentarioController.criar, methods=["POST"])
ComentarioController.blueprint.add_url_rule("/<int:comentario_id>", view_func=ComentarioController.buscar, methods=["GET"])
ComentarioController.blueprint.add_url_rule("/<int:comentario_id>", view_func=ComentarioController.atualizar, methods=["PUT"])
ComentarioController.blueprint.add_url_rule("/<int:comentario_id>", view_func=ComentarioController.deletar, methods=["DELETE"])
